FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Собираем статику с принудительным созданием директорий
RUN mkdir -p /app/staticfiles && \
    mkdir -p /app/static && \
    python manage.py collectstatic --noinput --clear && \
    chmod -R 755 /app/staticfiles

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "src.core.wsgi:application"]