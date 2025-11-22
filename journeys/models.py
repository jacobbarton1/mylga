import uuid

from django.conf import settings
from django.db import models

from fleet.models import Vehicle


class Journey(models.Model):
    MODE_CHOICES = [
        ("passive", "Passive (GPS-tracked vehicle)"),
        ("active", "Active (manual checkpoints)"),
    ]
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="journeys_created",
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journeys_as_driver",
    )
    buddy = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="journeys_as_buddy",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="journeys",
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    expected_end_time = models.DateTimeField()
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default="active")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="draft"
    )
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self) -> str:
        return f"{self.driver} to {self.destination} ({self.get_status_display()})"


class Checkpoint(models.Model):
    journey = models.ForeignKey(
        Journey, on_delete=models.CASCADE, related_name="checkpoints"
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    sequence = models.PositiveIntegerField()
    expected_time = models.DateTimeField()
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    checked_in_at = models.DateTimeField(null=True, blank=True)
    checked_in_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="checkpoints_checked",
    )

    class Meta:
        ordering = ["sequence"]

    def __str__(self) -> str:
        return f"{self.name} ({self.journey})"

    @property
    def is_complete(self) -> bool:
        return self.checked_in_at is not None


