FROM python:3.12-slim

# Install system deps for Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt && \
    playwright install chromium --with-deps

# Copy source
COPY pyproject.toml ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY entrypoint.sh ./entrypoint.sh

RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
