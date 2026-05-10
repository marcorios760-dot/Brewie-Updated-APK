# Build stage
FROM python:3.11-slim AS builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libserialport0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy pip dependencies from builder
COPY --from=builder /root/.local /root/.local

# Set PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY app ./app
COPY requirements.txt .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
