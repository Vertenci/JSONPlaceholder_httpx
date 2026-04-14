#!/bin/bash
set -e

echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

echo "Starting application..."
exec uvicorn src.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 14 \
  --loop uvloop \
  --http httptools \
  --limit-concurrency 2000 \
  --backlog 4096 \
  --limit-max-requests 50000 \
  --no-access-log
