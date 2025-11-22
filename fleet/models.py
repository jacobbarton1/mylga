from django.conf import settings
from django.db import models


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


class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name="maintenance_records"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="maintenance_created",
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


