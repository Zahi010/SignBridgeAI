# Stage 1: Build Frontend Assets
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Stage 2: Production Python Backend Runtime
FROM python:3.13-slim AS backend-runtime

WORKDIR /app

# System dependencies for OpenCV/MediaPipe and SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend source
COPY backend/ ./backend/
COPY scripts/ ./scripts/
COPY data/ ./data/

# Copy built frontend into static mount or dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure storage directories
RUN mkdir -p /app/data/sign_videos /app/data/avatar_animations /app/data/backups /app/data/uploads

ENV PYTHONUNBUFFERED=1
ENV SIGNBRIDGE_ENV=production
ENV SIGNBRIDGE_DEBUG=False

EXPOSE 8000

# Healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health/live || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

