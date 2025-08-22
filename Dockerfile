# DOM Tree Extraction - Production Dockerfile (Official Playwright Image)
# Fixed: Proper browser installation and permissions
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies as root
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Explicitly install Chromium browser as root user
RUN playwright install chromium

# Copy application code
COPY . .

# Create output and assets directories
RUN mkdir -p output assets

# Create non-root user with unique UID (avoiding conflicts)
RUN useradd -m -u 2000 scraper && \
    chown -R scraper:scraper /app

# Switch to non-root user AFTER all root operations
USER scraper

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1

# Default command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "1"]
