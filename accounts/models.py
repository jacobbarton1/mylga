from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    job_title = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=100, blank=True)
    require_profile_update = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"Profile for {self.user.get_username()}"


