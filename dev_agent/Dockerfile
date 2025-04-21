# ----------- Dev Agent Production Dockerfile -----------
FROM python:3.11-slim as base

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc build-essential && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m agentuser
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy agent source
COPY dev_agent ./dev_agent
COPY .env* ./  # Optional: bring in env files if present

# Healthcheck endpoint
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

# Switch to non-root
USER agentuser

# Expose default FastAPI port
EXPOSE 8000

# Entrypoint
CMD ["python", "-m", "dev_agent"]
