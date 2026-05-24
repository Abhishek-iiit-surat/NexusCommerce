# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app

# Install dependencies into a separate directory so we can copy only them later
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: Runtime ──────────────────────────────────────────────────────────
FROM python:3.10-slim AS runtime

# Create a non-root user — running as root inside a container is a security risk
RUN addgroup --system django && adduser --system --ingroup django django

WORKDIR /app

# Copy installed packages from builder stage (not re-installing, just copying)
COPY --from=builder /install /usr/local

# Copy application source code
COPY --chown=django:django . .

# Switch to non-root user
USER django

EXPOSE 8000

# Run migrations then start the dev server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8001"]
