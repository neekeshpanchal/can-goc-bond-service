# Dockerfile
FROM python:3.10-slim

# OS-level deps if needed (none required here)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# copy only requirements first for layer caching
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy application code
COPY app /app

# expose port and set minimal user
EXPOSE 5000

# Healthcheck (HTTP)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s CMD curl -f http://localhost:5000/health || exit 1

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app", "--workers", "2", "--threads", "4"]
