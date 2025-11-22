from django.conf import settings
from django.db import models


class ServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    spid = models.PositiveIntegerField(unique=True)
    primary_contact = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="primary_for_water",
    )

    def __str__(self) -> str:
        return self.name


class Scheme(models.Model):
    WATER_TYPE_CHOICES = [
        ("DW", "Drinking Water"),
        ("WW", "Waste Water"),
        ("RW", "Recycled Water"),
    ]
    service_provider = models.ForeignKey(
        ServiceProvider, on_delete=models.CASCADE, related_name="schemes"
    )
    type = models.CharField(max_length=2, choices=WATER_TYPE_CHOICES)
    description = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()

    def __str__(self) -> str:
        return f"{self.description} ({self.get_type_display()})"


class TestType(models.Model):
    description = models.CharField(max_length=255)
    units = models.CharField(max_length=50)
    limit = models.FloatField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=1.00)
    test_method = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.description


class TestPoint(models.Model):
    FREQUENCY_UNIT_CHOICES = [
        ("D", "Days"),
        ("W", "Weeks"),
        ("M", "Months"),
        ("Y", "Years"),
    ]
    reference = models.CharField(max_length=100)
    scheme = models.ForeignKey(
        Scheme, on_delete=models.CASCADE, related_name="test_points"
    )
    test_types = models.ManyToManyField(TestType, related_name="test_points")
    description = models.CharField(max_length=255)
    frequency = models.PositiveIntegerField()
    frequency_units = models.CharField(max_length=1, choices=FREQUENCY_UNIT_CHOICES)

    def __str__(self) -> str:
        return self.reference


class FieldSample(models.Model):
    test_point = models.ForeignKey(
        TestPoint, on_delete=models.CASCADE, related_name="samples"
    )
    collected_at = models.DateTimeField()
    collected_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="water_samples_collected",
    )

    def __str__(self) -> str:
        return f"Sample at {self.test_point.reference} on {self.collected_at:%Y-%m-%d %H:%M}"


class Laboratory(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class SampleCollection(models.Model):
    field_samples = models.ManyToManyField(FieldSample, related_name="collections")
    sent_at = models.DateTimeField()
    received_at = models.DateTimeField(null=True, blank=True)
    attachments = models.FileField(
        upload_to="sample_attachments/", null=True, blank=True
    )

    def __str__(self) -> str:
        return f"Collection sent {self.sent_at:%Y-%m-%d}"

    def is_complete(self) -> bool:
        return self.received_at is not None


class SampleResult(models.Model):
    field_sample = models.ForeignKey(
        FieldSample, on_delete=models.CASCADE, related_name="results"
    )
    test_type = models.ForeignKey(TestType, on_delete=models.CASCADE)
    value = models.FloatField()
    comments = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.test_type.description}: {self.value}"


class NonConformance(models.Model):
    STATUS_CHOICES = [
        ("AW", "Awaiting Action"),
        ("RN", "Regulator Notified"),
    ]
    sample_result = models.ForeignKey(
        SampleResult, on_delete=models.CASCADE, related_name="non_conformances"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return f"NC for {self.sample_result}"


class Incident(models.Model):
    STATUS_CHOICES = [
        ("A", "Active"),
        ("C", "Closed"),
    ]
    non_conformance = models.ForeignKey(
        NonConformance, on_delete=models.CASCADE, related_name="incidents"
    )
    incident_id = models.CharField(max_length=100, unique=True)
    occurred_at = models.DateTimeField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    def __str__(self) -> str:
        return f"Incident {self.incident_id}"


class IncidentCorrespondence(models.Model):
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="correspondences"
    )
    attachments = models.FileField(
        upload_to="incident_correspondence/", null=True, blank=True
    )
    date_time = models.DateTimeField()
    comments = models.TextField(blank=True)

    def __str__(self) -> str:
        return (
            f"Correspondence {self.date_time:%Y-%m-%d} - {self.incident.incident_id}"
        )


class CorrectiveAction(models.Model):
    STATUS_CHOICES = [
        ("NF", "Not Funded"),
        ("PL", "Planned"),
        ("CM", "Complete"),
    ]
    incident = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name="corrective_actions"
    )
    short_description = models.CharField(max_length=255)
    long_description = models.TextField()
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)
    estimated_delivery_date = models.DateField()
    actual_delivery_date = models.DateField(null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.short_description} ({self.get_status_display()})"


