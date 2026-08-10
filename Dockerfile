# Multi-stage Dockerfile

# Frontend builder (builds React client)
FROM node:18 AS frontend-builder
WORKDIR /app/client
COPY client/package*.json ./
RUN npm ci --silent
COPY client/ .
RUN npm run build

# Backend image
FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Copy built frontend into backend (optional serving)
COPY --from=frontend-builder /app/client/dist ./client/dist

# Expose port used by Cloud Run (8080)
EXPOSE 8080
ENV PORT=8080

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
