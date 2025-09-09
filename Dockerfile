# Dockerfile

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint script
COPY entrypoint.py /app/entrypoint.py
RUN chmod +x /app/entrypoint.py

# Copy application code
COPY . .

# Create media directory
RUN mkdir -p /app/media/uploads && chmod 755 /app/media

# Set environment variables
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=fhir_demo.settings
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING=utf-8

# Expose port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["python", "/app/entrypoint.py"]

# # Default command (will be passed to entrypoint)
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "arewa_backend.wsgi:application"]