import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create or update the local development administrator."

    @staticmethod
    def _require_env(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise CommandError(f"Missing required environment variable: {name}")
        return value

    @staticmethod
    def _bool_env(name: str, default: bool = False) -> bool:
        value = os.getenv(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    def handle(self, *args, **options):
        user_model = get_user_model()

        username = self._require_env("ADMIN_USER")
        email = os.getenv("ADMIN_EMAIL", "cla_admin@example.test")
        reset_password = self._bool_env("ADMIN_RESET_PASSWORD", default=False)

        user, created = user_model.objects.get_or_create(username=username)

        user.email = email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        if created or reset_password:
            password = self._require_env("ADMIN_PASSWORD")
            user.set_password(password)

        user.save()

        action = "Created" if created else "Updated"
        password_action = (
            "with password set"
            if created or reset_password
            else "without password reset"
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"{action} local administrator '{username}' {password_action}."
            )
        )
