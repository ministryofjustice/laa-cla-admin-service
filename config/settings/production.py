import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403


def required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise ImproperlyConfigured(
            f"The {name} environment variable must be configured."
        )

    return value


SECRET_KEY = required_env("DJANGO_SECRET_KEY")

DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": required_env("DATABASE_NAME"),
        "USER": required_env("DATABASE_USER"),
        "PASSWORD": required_env("DATABASE_PASSWORD"),
        "HOST": required_env("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": 60,
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")