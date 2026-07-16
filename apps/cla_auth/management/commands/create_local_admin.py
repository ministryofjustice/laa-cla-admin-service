import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or update the local development administrator."

    def handle(self, *args, **options):
        user_model = get_user_model()

        username = os.getenv("ADMIN_USER", "cla_admin")
        password = os.getenv("ADMIN_PASSWORD", "cla_admin")
        email = os.getenv("ADMIN_EMAIL", "cla_admin@example.test")

        user, created = user_model.objects.get_or_create(username=username)

        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        action = "Created" if created else "Updated"

        self.stdout.write(
            self.style.SUCCESS(
                f"{action} local administrator '{username}'."
            )
        )