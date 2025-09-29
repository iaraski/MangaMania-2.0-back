#!/bin/sh

# Ждём, пока база стартует
sleep 5

# Инициализация Alembic, если папки нет
if [ ! -d "./alembic" ]; then
  echo "Alembic not found, initializing..."
  alembic init alembic
fi

# Применяем все миграции
alembic upgrade head

# Запуск FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
