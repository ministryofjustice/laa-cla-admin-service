import os

from .base import *  # noqa: F403

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "cla_admin"),
        "USER": os.getenv("DATABASE_USER", "cla_admin"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", "cla_admin"),
        "HOST": os.getenv("DATABASE_HOST", "localhost"),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
    }
}
