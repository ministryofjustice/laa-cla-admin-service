# LAA CLA Admin Service

[![Ministry of Justice Repository Compliance Badge](https://github-community.service.justice.gov.uk/repository-standards/api/laa-cla-admin-service/badge)](https://github-community.service.justice.gov.uk/repository-standards/laa-cla-admin-service)

## Overview

The LAA CLA Admin Service is a Django-based microservice that replaces the legacy admin panel. It provides a modern administration interface for the Community Legal Advice backend, handling user authorization(?), permissions management, and reporting functionality.

## Features

- **Authorization & Permissions Management** - Centralized control over user access and role-based permissions
- **Reporting** - Generate and manage reports across the CLA system
- **Microservice Architecture** - Operates as a dedicated microservice for `cla_backend`
- **Modern Admin Interface** - Django-based administration panel replacing legacy systems
- **RESTful API** - Clean API for integration with other services

## Prerequisites

- Python 3.x
- Django 4.x+
- Virtual environment manager (venv/virtualenv)

## Installation

TODO

## Configuration

The service is configured via environment variables. See `.env.example` for available options.

## Usage

Access the admin panel at `http://localhost:8000/admin/` after starting the development server.

## Contributing

Please follow the [Ministry of Justice GitHub Repository Standards](https://github-community.service.justice.gov.uk/repository-standards/guidance).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
