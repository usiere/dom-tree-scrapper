#!/bin/bash
set -e

# Set the browser path explicitly
export PLAYWRIGHT_BROWSERS_PATH=/app/.cache/ms-playwright

# Create the directory if it does not exist
mkdir -p /app/.cache/ms-playwright

# Install Playwright browser and dependencies
echo "Installing Playwright browser to: $PLAYWRIGHT_BROWSERS_PATH"
playwright install chromium
playwright install-deps chromium

# Verify installation
echo "Verifying browser installation..."
ls -la /app/.cache/ms-playwright/

echo "Playwright browser installation completed successfully!"
