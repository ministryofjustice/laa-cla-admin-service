# LAA CLA Admin Service

[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/laa-cla-admin-service/badge)](https://github-community.service.justice.gov.uk/repository-standards/laa-cla-admin-service)

## Overview

The LAA CLA Admin Service provides a dedicated Django administration interface for Civil Legal Advice services.

The service is being extracted from `cla_backend` to reduce coupling between the CLA API and its administrative interface, and to support the wider migration towards independently deployable services.

The initial implementation uses Django's built-in user, group, and permission framework. SILAS authentication, reporting, additional CLA administration models, and service APIs will be added separately.

## Current functionality

- Django administration interface
- Local username and password authentication
- User management
- Group and permission management
- Health endpoint at `/status`
- PostgreSQL-backed local development environment
- Docker development and production images

## Planned functionality

- SILAS authentication
- CLA reporting
- Additional administration models migrated from `cla_backend`
- Service-to-service API integrations
- Role-based access policies
- Audit and operational monitoring improvements

## Project structure

    .
    ├── apps/
    │   ├── cla_auth/
    ├── config/
    │   └── settings/
    ├── docker/
    │   ├── Dockerfile
    │   └── compose.yaml
    ├── helm_deploy/
    ├── manage.py
    ├── pyproject.toml
    └── README.md

The `cla_auth` application owns the service's Django user model. It currently uses Django's standard authentication and permission behaviour and provides a foundation for future SILAS integration.

## Prerequisites

For the recommended Docker-based setup:

- Docker
- Docker Compose
- Git

A local Python installation is not required when using Docker.

For development outside Docker, use Python 3.14 (as declared in `pyproject.toml`).
## Local setup

Run:

    ./local-setup.sh

The setup script:

- creates `.env` from `.env.example` when required
- builds the Docker image
- starts PostgreSQL
- applies Django migrations
- creates or updates the local admin user
- starts the Django application

Local admin credentials:

- Username: `cla_admin`
- Password: `cla_admin`

Admin:

    http://localhost:8000/admin/

Health:

    http://localhost:8000/status

## Running without Docker

Create and activate a virtual environment:

    python -m venv .venv
    source .venv/bin/activate

Install the project and development dependencies:

    python -m pip install --upgrade pip
    python -m pip install -e ".[development]"

A PostgreSQL instance must be available and the database environment variables must be configured.

Apply migrations:

    python manage.py migrate

Create a local administrator:

    python manage.py createsuperuser

Start the development server:

    python manage.py runserver

## Environment variables

The service is configured using environment variables. See `.env.example` for local example values.

| Variable | Required | Description |
|---|---:|---|
| `DJANGO_SETTINGS_MODULE` | Yes | Django settings module to load |
| `SECRET_KEY` | Yes | Secret used by Django for cryptographic signing |
| `DEBUG` | No | Enables debug mode when set to a truthy value (`1`, `true`, `yes`, `on`) |
| `ALLOWED_HOSTS` | Yes | Comma-separated or whitespace-separated list of accepted hostnames |
| `DATABASE_NAME` | Yes | PostgreSQL database name |
| `DATABASE_USER` | Yes | PostgreSQL username |
| `DATABASE_PASSWORD` | Yes | PostgreSQL password |
| `DATABASE_HOST` | Yes | PostgreSQL host |
| `DATABASE_PORT` | No | PostgreSQL port; defaults to `5432` |

Production secrets must be supplied through the deployment platform and must not be stored in Helm values or committed to the repository.

## Authentication

The service currently uses Django's built-in local authentication.

Users with `is_staff` enabled can access the admin interface, subject to their assigned permissions. Local superusers have full access and are intended for development and initial setup only.

SILAS integration and production user provisioning will be implemented separately.

## Docker images

The Dockerfile is located at:

    docker/Dockerfile

It provides separate build targets:

- `development` — includes test and lint dependencies and runs Django's development server
- `production` — installs runtime dependencies and runs the application with Gunicorn

Build the production target locally with:

    docker build \
      --file docker/Dockerfile \
      --target production \
      --tag laa-cla-admin-service:local \
      .

The repository root must remain the Docker build context.

## Deployment

The service is deployed using the Helm chart in:

    helm_deploy/laa-cla-admin-service/

The application listens on port `8000`.

The existing Kubernetes liveness and readiness probes use:

    /status

Database migrations should be run as a dedicated deployment or release step, rather than automatically by every web container.

## Contributing

Please follow the [Ministry of Justice GitHub Repository Standards](https://github-community.service.justice.gov.uk/repository-standards/guidance).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
