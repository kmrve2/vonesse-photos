from flask import Flask, render_template, send_from_directory, jsonify
import os
import json
from pathlib import Path

app = Flask(__name__)

# Configure paths
PHOTOS_DIR = os.environ.get('PHOTOS_DIR', '/opt/data/vonesse-photos/photos')
THUMBNAILS_DIR = os.environ.get('THUMBNAILS_DIR', '/opt/data/vonesse-photos/thumbnails')
ALBUMS_FILE = Path('/opt/data/vonesse-photos/templates/albums.json')

def load_albums():
    """Load albums data from JSON."""
    if ALBUMS_FILE.exists():
        with open(ALBUMS_FILE) as f:
            return json.load(f)
    return []

@app.route('/')
def index():
    albums = load_albums()
    return render_template('index.html', albums=albums)

@app.route('/photos/<path:filename>')
def serve_photo(filename):
    return send_from_directory(PHOTOS_DIR, filename)

@app.route('/thumbnails/<path:filename>')
def serve_thumbnail(filename):
    return send_from_directory(THUMBNAILS_DIR, filename)

@app.route('/album/<slug>')
def album_page(slug):
    """Serve an album page."""
    albums = load_albums()
    for album in albums:
        if album['slug'] == slug:
            return render_template('album.html', album=album)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)