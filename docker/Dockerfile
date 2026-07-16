FROM python:3.14-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY manage.py ./
COPY config ./config
COPY apps ./apps
COPY bin ./bin

RUN python -m pip install --upgrade pip


FROM base AS development

RUN python -m pip install -e ".[development]"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


FROM base AS production

RUN python -m pip install .

RUN addgroup -g 1000 django \
    && adduser -D -u 1000 -G django django

COPY --chown=django:django . .

RUN DJANGO_SETTINGS_MODULE=config.settings.production \
    DJANGO_SECRET_KEY=build-only-secret \
    DJANGO_ALLOWED_HOSTS=localhost \
    python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-"]
