# Minimal image used to exercise CI/CD pipelines for this repository.
FROM python:3.12-alpine AS base

WORKDIR /app

# Serve a basic health endpoint at /status expected by the Helm probes.
RUN printf 'ok\n' > status && \
    printf '<!doctype html><html><body><h1>laa-cla-admin-service</h1></body></html>\n' > index.html

EXPOSE 8000

FROM base AS production

CMD ["python", "-m", "http.server", "8000", "--bind", "0.0.0.0"]
