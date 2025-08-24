#!/bin/bash

echo "🚀 Starting Google Maps Scraper deployment..."

# Set environment variables
export PYTHONPATH="/app:$PYTHONPATH"
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Chrome environment variables
export CHROME_BIN="/nix/store/*/bin/chromium"
export CHROMEDRIVER_PATH="/nix/store/*/bin/chromedriver"

echo "📦 Checking Python and pip versions..."
python --version
pip --version

echo "📋 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🔍 Verifying installations..."
python -c "import fastapi; print('✅ FastAPI installed')"
python -c "import selenium; print('✅ Selenium installed')"
python -c "import lxml; print('✅ lxml installed')"
python -c "import requests; print('✅ requests installed')"

echo "🌐 Testing Chrome availability..."
which chromium || echo "⚠️ Chromium not found in PATH"
which chromedriver || echo "⚠️ ChromeDriver not found in PATH"

echo "🎯 Starting the application..."
python simple_app.py
