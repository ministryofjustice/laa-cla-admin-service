from .base import *  # noqa: F403

# TEMPORARY: UAT-specific settings using SQLite until a dedicated DB instance is provisioned
# TODO: Once UAT DB is ready, replace this file with correct pattern
# and configure DATABASE_* env vars in helm_deploy/laa-cla-admin-service/values/values-uat.yaml

# TEMPORARY: SQLite database - will be replaced with PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/app/data/db.sqlite3",
    }
}
