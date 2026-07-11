# Vonesse Photos

A family photo gallery website showcasing memories from the Vonesse family.

## Albums

- **Działka** - Family cottage and garden photos
- **Pets** - Doodle, Beans, Figaro, and Macchiato  
- **Projects** - Builds and creations

## Installation

### One-Command Install (Ubuntu/Debian)
Run this single command on your server:
```bash
sudo bash -c "$(curl -fsSL https://raw.githubusercontent.com/kmrve2/vonesse-photos/main/install.sh)"
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
   git clone https://github.com/kmrve2/vonesse-photos.git
   cd vonesse-photos
   ```
3. **Run the installer**:
   ```bash
   sudo bash install.sh
   ```

## Tech

- Static HTML/CSS/JS
- GitHub Pages hosting
- Lazy loading for performance
- Responsive design
- Lightbox viewer

## License

Private family project