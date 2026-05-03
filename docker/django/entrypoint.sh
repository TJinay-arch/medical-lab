#!/bin/sh

echo "⏳ Waiting for Postgres..."

while ! nc -z db 5432; do
  sleep 1
done

echo "✅ Postgres is up"

echo "📦 Migrations..."
python manage.py migrate --noinput

echo "🧹 Collectstatic..."
python manage.py collectstatic --noinput

echo "🚀 Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000