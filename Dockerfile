# Multi-stage Rootless Dockerfile for PrecisionX OIML R-76 Suite
FROM python:3.11-slim as builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libzbar0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app/src:/app/backend:$PYTHONPATH

COPY . /app

EXPOSE 8000
CMD ["uvicorn", "api.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000"]
