import os

from .base import *  # noqa: F403

DEBUG = True

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-development-only",
)

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/app/data/db.sqlite3",
    }
}
