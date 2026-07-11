#!/bin/bash
# Photo Gallery - One-Command Installer
# Usage: sudo bash install.sh

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

APP_DIR="/var/www/photo-gallery"
PHOTOS_DIR="/var/www/photos"
SMB_USER="uploader"

echo -e "${BLUE}Starting Photo Gallery Installation...${NC}"

# 1. Update and Install Dependencies
echo -e "${GREEN}[1/7] Updating system and installing dependencies...${NC}"
apt update && apt upgrade -y
apt install -y git nginx samba python3 python3-pip python3-venv curl ufw

# Configure Firewall
echo "Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow samba
ufw --force enable

# 2. Create Directories
echo -e "${GREEN}[2/7] Creating directories...${NC}"
mkdir -p "$APP_DIR"
mkdir -p "$PHOTOS_DIR"

# 3. Clone Repository (if not already there)
if [ ! -f "$APP_DIR/app.py" ]; then
    echo -e "${GREEN}[3/7] Cloning repository...${NC}"
    GIT_TERMINAL_PROMPT=0 git clone https://github.com/kmrve2/vonesse-photos.git "$APP_DIR"
else
    echo -e "${GREEN}[3/7] Repository already exists, skipping clone...${NC}"
    cd "$APP_DIR"
    git pull origin main
fi

cd "$APP_DIR"

# 4. Set Up Python
echo -e "${GREEN}[4/7] Setting up Python environment...${NC}"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt

# 5. Configure Nginx
echo -e "${GREEN}[5/7] Configuring Nginx...${NC}"
cp nginx/photo-gallery.conf /etc/nginx/sites-available/photo-gallery
ln -sf /etc/nginx/sites-available/photo-gallery /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

# 6. Configure Samba
echo -e "${GREEN}[6/7] Configuring Samba...${NC}"

# Ensure Samba config directory exists
mkdir -p /etc/samba/smbconf.d

# Copy the config
cp samba/photo-gallery.conf /etc/samba/smbconf.d/photo-gallery.conf

# Ensure Samba includes this directory in the main config
if ! grep -q "include = /etc/samba/smbconf.d/*.conf" /etc/samba/smb.conf; then
    echo "include = /etc/samba/smbconf.d/*.conf" >> /etc/samba/smb.conf
fi

# Add user if not exists
if ! id "$SMB_USER" &>/dev/null; then
    useradd -M -s /usr/sbin/nologin "$SMB_USER"
fi

# Set Samba password
echo "Setting Samba password for user '$SMB_USER'..."
echo "Note: Password must be at least 8 characters long."
echo "Press Enter to use a random password, or type a password below:"
read -s -p "SMB Password: " SMB_PASS
if [ -z "$SMB_PASS" ]; then
    SMB_PASS=$(openssl rand -base64 12)
    echo "(Generated random password: $SMB_PASS)"
fi
echo -e "${SMB_PASS}\n${SMB_PASS}" | smbpasswd -a -s "$SMB_USER"

systemctl restart smbd nmbd

# 7. Set Up Systemd Service
echo -e "${GREEN}[7/7] Setting up Systemd service...${NC}"

# Check that required files exist
if [ ! -f "gunicorn.conf.py" ]; then
    echo "ERROR: gunicorn.conf.py not found. Aborting."
    exit 1
fi

cat > /etc/systemd/system/photo-gallery.service << EOF
[Unit]
Description=Photo Gallery
After=network.target nginx.service smbd.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment="PATH=$APP_DIR/.venv/bin"
ExecStart=$APP_DIR/scripts/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable photo-gallery

# Ensure start script is executable
chmod +x "$APP_DIR/scripts/start.sh"

# Set permissions BEFORE starting the service
chown -R www-data:www-data "$APP_DIR"
chown -R www-data:www-data "$PHOTOS_DIR"

systemctl start photo-gallery

echo -e "${BLUE}Installation Complete!${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📸  Next Steps"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "  1. View the gallery:"
echo "     http://<YOUR_SERVER_IP>"
echo ""
echo "  2. Add photos via SMB share:"
echo "     URL:   smb://<YOUR_SERVER_IP>/photo-gallery"
echo "     User:  $SMB_USER"
echo "     Pass:  (the one you just set)"
echo ""
echo "  3. The gallery updates automatically when the service restarts."
echo "     To force an update now:"
echo "     systemctl restart photo-gallery"
echo ""
echo "  4. To test with a sample photo:"
echo "     cp -r /var/www/photo-gallery/sample-photos/* /var/www/photos/"
echo "     systemctl restart photo-gallery"
echo ""
echo "  5. To change the SMB password later:"
echo "     smbpasswd $SMB_USER"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"