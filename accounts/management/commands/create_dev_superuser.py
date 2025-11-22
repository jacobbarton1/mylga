from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = (
        "Create or update the development superuser "
        "jacob_barton@murweh.qld.gov.au with password '1234'."
    )

    def handle(self, *args, **options) -> None:
        User = get_user_model()
        email = "jacob_barton@murweh.qld.gov.au"
        username = email
        password = "1234"

        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.email = email
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    "Created development superuser jacob_barton@murweh.qld.gov.au"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Updated development superuser jacob_barton@murweh.qld.gov.au"
                )
            )

