FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir uv && \
    uv pip install -r requirements.txt

CMD ["uvicorn", "core.asgi:application", "--host", "0.0.0.0", "--port", "8000"]