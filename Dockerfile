FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of app files
COPY . .

# Create non-root user and switch to it
RUN useradd --create-home appuser
USER appuser

# Expose port
EXPOSE 5050

# Run gunicorn
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:5050", "run:app"]
