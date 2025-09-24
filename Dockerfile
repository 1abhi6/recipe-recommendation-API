# Use official lightweight Python image (supports Python 3.12)
FROM python:3.12-slim AS base

# Set environment variables (prevent Python from writing .pyc & ensure stdout/stderr are unbuffered)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (for building some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user for security
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Copy dependency files first (leverage Docker cache)
COPY pyproject.toml uv.lock* ./

# Install dependencies using pip (PEP 621 compatible with pyproject.toml)
RUN pip install --upgrade pip \
    && pip install .

# Copy project files (but not .env, thanks to .dockerignore)
COPY src ./src
COPY main.py ./
COPY README.md ./

# Switch to non-root user
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]