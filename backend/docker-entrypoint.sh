#!/bin/sh
set -eu

echo "Ожидание PostgreSQL и подготовка схем..."
python -c "import main; print('Схемы PostgreSQL готовы')"

if [ "${SEED_DEMO_DATA:-true}" = "true" ]; then
  echo "Обновление демонстрационных данных..."
  python seed.py
fi

echo "Запуск S-Art API..."
exec uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers "${WEB_CONCURRENCY:-2}" \
  --log-config /app/uvicorn-log-config.json

