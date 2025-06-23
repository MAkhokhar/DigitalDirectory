# Use official Python slim image (smaller + more secure)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Create and switch to user (avoid root)
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app
WORKDIR /app
USER appuser

# Install dependencies first (better layer caching)
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Specify the command to run
CMD ["python", "./app.py"]
