#!/bin/sh
set -e

echo "==> Running migrations..."
python scripts/migrate.py

echo "==> Running seed..."
python scripts/seed.py

echo "==> Starting server..."
exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT:-8000}"
