#!/usr/bin/env bash
set -e

echo "Starting VAULT Core Production Engine..."

if [ -n "$DATABASE_URL" ]; then
    echo "Running database migrations..."
    python -m alembic -c backend/alembic.ini upgrade head || {
        echo "Warning: Database migration failed. Continuing startup..."
    }
else
    echo "DATABASE_URL not set. Running in liveness-only mode."
fi

PORT="${PORT:-8000}"
echo "Listening on port $PORT..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port "$PORT"
