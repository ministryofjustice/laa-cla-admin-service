import os

from .base import *  # noqa: F403
from .base import MIDDLEWARE as BASE_MIDDLEWARE

# TEMPORARY: UAT-specific settings using SQLite until a dedicated DB instance is provisioned
# TODO: Once UAT DB is ready, replace this file with correct pattern
# and configure DATABASE_* env vars in helm_deploy/laa-cla-admin-service/values/values-uat.yaml

DEBUG = True

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-local-development-only",
)

ALLOWED_HOSTS = ["*"]

# CSRF: For UAT, trust all Cloud Platform domains (includes dynamic release names)
# Pattern matches lga-4146-setup-admin-service-laa-cla-admin-service-uat.cloud-platform.service.justice.gov.uk
CSRF_TRUSTED_ORIGINS = [
    "https://*.cloud-platform.service.justice.gov.uk",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
] + BASE_MIDDLEWARE[1:]

# TEMPORARY: SQLite database - will be replaced with PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/app/data/db.sqlite3",
    }
}
