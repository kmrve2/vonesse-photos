from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import json
from pathlib import Path

app = Flask(__name__)

# Configure paths
PHOTOS_DIR = os.environ.get('PHOTOS_DIR', '/var/www/photos')
THUMBNAILS_DIR = os.environ.get('THUMBNAILS_DIR', '/var/www/photo-gallery/thumbnails')
ALBUMS_FILE = Path('/var/www/photo-gallery/templates/albums.json')

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

@app.route('/api/refresh', methods=['POST'])
def refresh_gallery():
    """API endpoint to trigger gallery regeneration."""
    import subprocess
    import os
    
    # Simple auth check (you can change 'frank' to whatever you want)
    data = request.get_json()
    if not data or data.get('secret') != 'frank':
        return jsonify({'error': 'Invalid secret'}), 401
    
    try:
        # Run the generator script
        result = subprocess.run(
            ['python3', 'generate-gallery.py'],
            cwd='/var/www/photo-gallery',
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return jsonify({'status': 'success', 'message': 'Gallery updated!'})
        else:
            return jsonify({'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)