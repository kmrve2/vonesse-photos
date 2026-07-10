#!/usr/bin/env python3
"""
Vonesse Photos - Gallery Generator

Scans the photos/ directory and generates the gallery HTML.
Usage: python3 generate-gallery.py
"""
import os
import json
from pathlib import Path

PHOTOS_DIR = Path("photos")
OUTPUT_FILE = Path("js/gallery-data.json")

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
        for ext in [".jpg", ".jpeg", ".png", ".webp"]:
            photos.extend(album_dir.glob(f"*{ext}"))
        
        # Skip cover images from the main list
        photos = [p for p in photos if p.name.lower() != "cover.jpg"]
        photos.sort()
        
        # Find cover image
        cover = None
        for ext in ["cover.jpg", "cover.png", "cover.webp"]:
            cover_path = album_dir / ext
            if cover_path.exists():
                cover = f"photos/{album_dir.name}/{cover_path.name}"
                break
        
        # If no cover, use first photo
        if not cover and photos:
            cover = f"photos/{album_dir.name}/{photos[0].name}"
        
        album_data = {
            "name": album_name,
            "slug": album_dir.name,
            "cover": cover,
            "photos": [f"photos/{album_dir.name}/{p.name}" for p in photos]
        }
        
        albums.append(album_data)
    
    return albums

def generate():
    """Generate gallery data JSON."""
    albums = scan_photos()
    
    # Write JSON data file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(albums, f, indent=2)
    
    print(f"Generated gallery with {len(albums)} albums")
    for album in albums:
        print(f"  - {album['name']}: {len(album['photos'])} photos")

if __name__ == "__main__":
    generate()