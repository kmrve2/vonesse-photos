#!/usr/bin/env python3
"""
Vonesse Photos - Gallery Generator

Scans the photos/ directory and generates the gallery HTML.
Usage: python3 generate-gallery.py
"""
import os
import json
from pathlib import Path
from PIL import Image

PHOTOS_DIR = Path(os.environ.get('PHOTOS_DIR', '/opt/data/vonesse-photos/photos'))
THUMBNAILS_DIR = Path('/opt/data/vonesse-photos/thumbnails')
OUTPUT_FILE = Path('/opt/data/vonesse-photos/templates/albums.json')

def generate_thumbnail(photo_path, album_slug):
    """Generate a thumbnail for a photo."""
    thumb_dir = THUMBNAILS_DIR / album_slug
    thumb_dir.mkdir(parents=True, exist_ok=True)
    
    thumb_path = thumb_dir / f"{photo_path.stem}_thumb.jpg"
    
    if not thumb_path.exists():
        try:
            with Image.open(photo_path) as img:
                # Convert to RGB if necessary (handles RGBA, etc.)
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Resize to max 400px width/height
                img.thumbnail((400, 400), Image.Resampling.LANCZOS)
                img.save(thumb_path, 'JPEG', quality=85)
        except Exception as e:
            print(f"Error generating thumbnail for {photo_path}: {e}")
    
    return f"thumbnails/{album_slug}/{thumb_path.name}"

def scan_photos():
    """Scan photos/ directory and return album structure."""
    albums = []
    
    if not PHOTOS_DIR.exists():
        return albums
    
    for album_dir in sorted(PHOTOS_DIR.iterdir()):
        if not album_dir.is_dir():
            continue
            
        album_name = album_dir.name.replace("-", " ").title()
        photos = []
        
        # Get all image files
        for ext in [".jpg", ".jpeg", ".png", ".webp", ".heic"]:
            photos.extend(album_dir.glob(f"*{ext}"))
        
        # Skip cover images from the main list
        photos = [p for p in photos if p.name.lower() not in ["cover.jpg", "cover.png", "cover.webp"]]
        photos.sort()
        
        # Find cover image
        cover = None
        for ext in ["cover.jpg", "cover.png", "cover.webp"]:
            cover_path = album_dir / ext
            if cover_path.exists():
                cover = generate_thumbnail(cover_path, album_dir.name)
                break
        
        # If no cover, use first photo
        if not cover and photos:
            cover = generate_thumbnail(photos[0], album_dir.name)
        
        # Generate thumbnails for all photos
        photo_thumbnails = []
        for photo in photos:
            thumb = generate_thumbnail(photo, album_dir.name)
            photo_thumbnails.append({
                "original": f"photos/{album_dir.name}/{photo.name}",
                "thumbnail": thumb
            })
        
        album_data = {
            "name": album_name,
            "slug": album_dir.name,
            "cover": cover,
            "photos": photo_thumbnails,
            "photo_count": len(photo_thumbnails)
        }
        
        albums.append(album_data)
    
    return albums

def generate():
    """Generate gallery data JSON."""
    albums = scan_photos()
    
    # Write JSON data file for Flask
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(albums, f, indent=2)
    
    print(f"Generated gallery with {len(albums)} albums")
    for album in albums:
        print(f"  - {album['name']}: {album['photo_count']} photos")

if __name__ == "__main__":
    generate()