from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


def maintenance_evidence_upload_to(instance, filename):
    record = None
    if hasattr(instance, "maintenance_record") and instance.maintenance_record_id:
        record = instance.maintenance_record
    elif hasattr(instance, "vehicle") and instance.vehicle_id:
        record = instance
    date = getattr(record, "date", None) or timezone.now().date()
    unit_number = None
    if record and record.vehicle_id:
        unit_number = record.vehicle.unit_number
    unit_folder = f"{int(unit_number):04d}" if unit_number is not None else "unassigned"
    return f"fleet/maintenance/{unit_folder}/{date.year}/{date.month:02d}/{filename}"


class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ("light", "Light Vehicle"),
        ("heavy", "Heavy Vehicle"),
        ("plant", "Plant"),
        ("trailer", "Trailer"),
        ("other", "Other"),
    ]

    unit_number = models.PositiveIntegerField(unique=True)
    registration = models.CharField(max_length=20, blank=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="other"
    )
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    department = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["unit_number"]

    def __str__(self) -> str:
        return f"Unit {self.unit_number:04d} - {self.registration or 'unregistered'}"


class DefectReport(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="defects"
    )
    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="defects_reported",
    )
    reported_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    severity = models.CharField(
        max_length=10, choices=SEVERITY_CHOICES, default="low"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="open"
    )
    workshop_notes = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-reported_at"]

    def __str__(self) -> str:
        return f"Defect on {self.vehicle} ({self.get_severity_display()})"

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = (
                DefectReport.objects.filter(pk=self.pk)
                .values_list("status", flat=True)
                .first()
            )
        super().save(*args, **kwargs)
        if (
            previous_status is not None
            and previous_status != self.status
            and self.reported_by
            and self.reported_by.email
        ):
            self._email_status_change(previous_status)

    def _email_status_change(self, previous_status: str) -> None:
        subject = f"Fleet defect update for unit {self.vehicle.unit_number}"
        message = (
            "Hello,\n\n"
            f"The defect you reported for {self.vehicle} has changed status "
            f"from '{self.get_status_display_value(previous_status)}' "
            f"to '{self.get_status_display()}'.\n\n"
            "Latest workshop notes:\n"
            f"{self.workshop_notes or 'No notes added.'}\n\n"
            "You will receive further updates as the status changes."
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.reported_by.email],
            fail_silently=True,
        )

    def get_status_display_value(self, value: str) -> str:
        return dict(self.STATUS_CHOICES).get(value, value)


class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="maintenance_records"
    )
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_submitted",
    )
    defect_report = models.ForeignKey(
        DefectReport,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_records",
    )
    date = models.DateField()
    description = models.TextField()
    odometer_km = models.PositiveIntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.vehicle} maintenance on {self.date}"


class MaintenanceEvidence(models.Model):
    maintenance_record = models.ForeignKey(
        MaintenanceRecord,
        on_delete=models.CASCADE,
        related_name="evidence_documents",
    )
    file = models.FileField(upload_to=maintenance_evidence_upload_to)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="maintenance_evidence_uploaded",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return (
            f"Evidence for {self.maintenance_record.vehicle} on "
            f"{self.maintenance_record.date}"
        )
