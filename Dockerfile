# 1. Use the official Python 3.13 image as the base
FROM python:3.12-slim

# 2. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 3. Install uv (modern Python package manager)
RUN pip install --no-cache-dir uv

# 4. Set working directory
WORKDIR /app

# 5. Copy project files
COPY pyproject.toml uv.lock ./
COPY . .

# 6. Ensure .env is ignored (security best practice)
# The .env should be mounted as a secret or via environment variables

# 7. Install dependencies using uv
RUN uv pip install --system --no-deps --sync

# 8. Expose FastAPI port
EXPOSE 8000

# 9. Set environment variables for production
ENV PYTHONUNBUFFERED=1
ENV UVICORN_WORKERS=1

# 10. Default command to run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]