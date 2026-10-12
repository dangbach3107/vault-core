# ==========================================
# Stage 1: Build Frontend (React + Vite)
# ==========================================
FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
COPY contracts/ /app/contracts/
RUN npm run build

# ==========================================
# Stage 2: Production Runner (Python + FastAPI)
# ==========================================
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENVIRONMENT=production \
    INTERNAL_PREVIEW_ENABLED=true \
    ALLOW_PUBLIC_ACCESS=true

# Install dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend code, migrations, and scripts
COPY backend/ ./backend/
COPY contracts/ ./contracts/
COPY scripts/start-production.sh ./scripts/start-production.sh

# Copy built frontend from Stage 1 into /app/frontend/dist
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create upload directory
RUN mkdir -p .data/uploads && chmod +x scripts/start-production.sh

EXPOSE 8000

CMD ["./scripts/start-production.sh"]
