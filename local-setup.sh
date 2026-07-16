#!/usr/bin/env bash

set -euo pipefail

export DOCKER_BUILDKIT=1
export ENVIRONMENT="${1:-development}"

COMPOSE_FILE="docker/compose.yaml"

echo "Running environment: ${ENVIRONMENT}"

docker compose -f "${COMPOSE_FILE}" down --remove-orphans
docker compose -f "${COMPOSE_FILE}" build web
docker compose -f "${COMPOSE_FILE}" up -d db

docker compose -f docker/compose.yaml run --rm web bin/create_db.sh

docker compose -f "${COMPOSE_FILE}" up web