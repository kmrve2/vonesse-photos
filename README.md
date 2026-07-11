# Photo Gallery

A self-hosted photo gallery application for organizing and sharing family memories.

## Features

- **Albums**: Organize photos by category.
- **Lightbox**: Click to view full-size with navigation.
- **Responsive**: Looks great on phone, tablet, desktop.
- **Lazy Loading**: Pages load fast even with lots of photos.
- **Easy Updates**: Drop photos in a folder, and the gallery updates automatically.

## Installation

### One-Command Install (Ubuntu/Debian)
Run this single command on your server:
```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/USER/REPO/main/install.sh)"
```

### Manual Install
1. **Update and install dependencies**:
   ```bash
   apt update && apt upgrade -y
   apt install -y git nginx samba python3 python3-pip python3-venv curl
   ```
2. **Clone the repository**:
   ```bash
   mkdir -p /var/www && cd /var/www
   git clone https://github.com/USER/REPO.git photo-gallery
   cd photo-gallery
   ```
3. **Run the installer**:
   ```bash
   sudo bash install.sh
   ```

## Adding Photos

Drop photos into the `/var/www/photos` folder organized by album:
```
/var/www/photos/
├── album-one/
│   ├── photo1.jpg
│   └── cover.jpg
├── album-two/
│   ├── photo1.jpg
│   └── cover.jpg
```

Then run `python3 generate-gallery.py` to update the gallery.

## Tech

- Static HTML/CSS/JS
- Flask backend
- Gunicorn WSGI server
- Nginx reverse proxy
- Samba for network file sharing
- Pillow for image optimization

## License

Private family project