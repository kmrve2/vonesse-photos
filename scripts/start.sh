#!/bin/bash
# Vonesse Photos - Startup Script
# This script pulls the latest code from GitHub and starts all services

set -e

APP_DIR="/var/www/vonesse-photos"
PHOTOS_DIR="/var/www/photos"
LOG_DIR="/var/log/vonesse-photos"

# Create necessary directories
mkdir -p "$LOG_DIR"
mkdir -p "$PHOTOS_DIR"

# Pull latest code from GitHub
echo "Pulling latest code from GitHub..."
cd "$APP_DIR"
git pull origin main

# Install Python dependencies
echo "Installing Python dependencies..."
source "$APP_DIR/.venv/bin/activate"
pip install -r "$APP_DIR/requirements.txt"

# Generate gallery from photos
echo "Generating gallery..."
python3 "$APP_DIR/generate-gallery.py"

# Start Gunicorn
echo "Starting Gunicorn..."
cd "$APP_DIR"
source "$APP_DIR/.venv/bin/activate"
gunicorn -c "$APP_DIR/gunicorn.conf.py" app:app &

# Start Nginx
echo "Starting Nginx..."
nginx

# Start Samba
echo "Starting Samba..."
smbd -D

echo "Vonesse Photos started successfully!"
echo "Access the gallery at: http://<LXC-IP>"
echo "Add photos via SMB: smb://<LXC-IP>/vonesse-photos"