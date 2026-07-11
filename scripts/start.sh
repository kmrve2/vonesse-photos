#!/bin/bash
# Wrapper script: Regenerate gallery then start Gunicorn
cd /var/www/photo-gallery
source .venv/bin/activate

# 1. Regenerate gallery from photos
echo "Regenerating gallery..."
python3 generate-gallery.py

# 2. Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn -c gunicorn.conf.py app:app