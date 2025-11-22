from django.conf import settings
from django.db import models
from django.utils import timezone


class FloodSite(models.Model):
    handle = models.CharField(
        max_length=50,
        unique=True,
        help_text="Short station handle or ID used in URLs.",
    )
    name = models.CharField(max_length=255, help_text="Display name for the site.")
    location_description = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    active = models.BooleanField(default=True)

    imei = models.CharField(
        max_length=32,
        blank=True,
        help_text="Optional IMEI or device identifier used in payloads.",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="flood_sites",
    )

    trigger_low_low_mm = models.IntegerField(
        null=True,
        blank=True,
        help_text="Distance (mm) at or below which bed is considered dry.",
    )
    trigger_low_mm = models.IntegerField(
        null=True,
        blank=True,
        help_text="Distance (mm) above dry bed where water is first detected.",
    )
    trigger_high_mm = models.IntegerField(
        null=True,
        blank=True,
        help_text="Distance (mm) where water over road is likely.",
    )
    trigger_high_high_mm = models.IntegerField(
        null=True,
        blank=True,
        help_text="Distance (mm) where water over road is significant.",
    )

    class Meta:
        ordering = ["handle"]

    def __str__(self) -> str:
        return f"{self.name} [{self.handle}]"

    def level_state_for_distance(self, distance_mm: int | None) -> str:
        if distance_mm is None:
            return "unknown"

        low_low = self.trigger_low_low_mm
        low = self.trigger_low_mm
        high = self.trigger_high_mm
        high_high = self.trigger_high_high_mm

        if high_high is not None and distance_mm >= high_high:
            return "high_high"
        if high is not None and distance_mm >= high:
            return "high"
        if low_low is not None and distance_mm <= low_low:
            return "low_low"
        if low is not None and distance_mm <= low:
            return "low"
        return "unknown"


class Uplink(models.Model):
    site = models.ForeignKey(
        FloodSite, on_delete=models.CASCADE, related_name="uplinks"
    )
    distance_mm = models.IntegerField(help_text="Measured distance in mm.")
    battery_v = models.FloatField(null=True, blank=True)
    signal_dbm = models.IntegerField(null=True, blank=True)
    received_at = models.DateTimeField(default=timezone.now)
    raw_payload = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self) -> str:
        return f"{self.site.handle} at {self.received_at}"

    @property
    def level_state(self) -> str:
        return self.site.level_state_for_distance(self.distance_mm)


