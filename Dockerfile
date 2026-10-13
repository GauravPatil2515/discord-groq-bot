# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY bot.py .
COPY test_credentials.py .

# Run as non-root user for security
RUN useradd -m botuser && chown -R botuser /app
USER botuser

CMD ["python", "bot.py"]
