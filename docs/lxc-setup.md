# Vonesse Photos - LXC Setup Guide

## Prerequisites
- Proxmox VE installed and running
- Access to Proxmox web interface or CLI
- Local network range: `192.168.1.x`

## Step 1: Create the LXC Container

### Via Proxmox Web Interface:
1. Go to your Proxmox node
2. Click "CT" (Containers) → "Create Container"
3. **OS**: Select "Debian 12" (or Ubuntu 22.04)
4. **General**:
   - Container ID: `100` (or any available ID)
   -_hostname: `vonesse-photos`
5. **Root Disk**:
   - Size: `8GB` (plenty for the app)
   - Storage: Select your preferred storage
6. **CPU**:
   - Cores: `1`
   - Limit: `100`
7. **Memory**:
   - Memory: `512MB`
8. **Network**:
   - Bridge: `vmbr0` (or your network bridge)
   - DHCP: Enable (or set static IP)
9. **Features**:
   - Nesting: `Yes` (needed for some packages)
   - Keyctl: `Yes`
10. Click "Finish"

### Via CLI:
```bash
pct create 100 local:vztmpl/debian-12-default-stretch.tar.gz \
  --hostname vonesse-photos \
  --memory 512 \
  --cores 1 \
  --net0 name=eth0,bridge=vmbr0,ip=dhcp \
  --features nesting=1,keyctl=1
```

## Step 2: Configure the Container

### SSH into the container:
```bash
pct start 100
pct console 100
```

### Update and install dependencies:
```bash
apt update && apt upgrade -y
apt install -y git nginx samba python3 python3-pip python3-venv curl
```

## Step 3: Set Up the Application

### Create directories:
```bash
mkdir -p /var/www/vonesse-photos
mkdir -p /var/www/photos
mkdir -p /var/log/vonesse-photos
```

### Clone the repository:
```bash
cd /var/www/vonesse-photos
git clone https://github.com/kmrve2/vonesse-photos.git .
```

### Set up Python virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Generate initial gallery:
```bash
python3 generate-gallery.py
```

## Step 4: Configure Nginx

### Copy the config:
```bash
cp /var/www/vonesse-photos/nginx/vonesse-photos.conf /etc/nginx/sites-available/vonesse-photos
ln -s /etc/nginx/sites-available/vonesse-photos /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default  # Remove default site
```

### Test and restart Nginx:
```bash
nginx -t  # Test config
systemctl restart nginx
```

## Step 5: Configure Samba

### Copy the config:
```bash
cp /var/www/vonesse-photos/samba/vonesse-photos.conf /etc/samba/smbconf.d/vonesse-photos.conf
```

### Add Frank as a Samba user:
```bash
useradd -M -s /usr/sbin/nologin frank
smbpasswd -a frank
# Enter a password for Frank
```

### Restart Samba:
```bash
systemctl restart smbd nmbd
```

## Step 6: Set Up Auto-Start

### Create a systemd service:
```bash
cat > /etc/systemd/system/vonesse-photos.service << EOF
[Unit]
Description=Vonesse Photos Gallery
After=network.target nginx.service smbd.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/vonesse-photos
Environment="PATH=/var/www/vonesse-photos/.venv/bin"
ExecStart=/var/www/vonesse-photos/.venv/bin/gunicorn -c gunicorn.conf.py app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```

### Enable and start the service:
```bash
systemctl daemon-reload
systemctl enable vonesse-photos
systemctl start vonesse-photos
```

## Step 7: Configure Firewall (if needed)

### Allow HTTP and SMB traffic:
```bash
# If using ufw
ufw allow 80/tcp
ufw allow 445/tcp
ufw allow 137:138/udp

# If using iptables
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 445 -j ACCEPT
iptables -A INPUT -p udp --dport 137:138 -j ACCEPT
```

## Step 8: Test the Setup

### From your local network:
1. **Find the LXC IP**: `ip addr show eth0`
2. **Access the gallery**: `http://<LXC-IP>`
3. **Test SMB share** (from Frank's Mac):
   - Open Finder → Go → Connect to Server
   - Enter: `smb://<LXC-IP>/vonesse-photos`
   - Username: `frank`
   - Password: (the one you set)

## Step 9: Update Workflow

### To update the site:
1. Make changes in this container
2. Push to GitHub: `git push origin main`
3. In the LXC: `cd /var/www/vonesse-photos && git pull && python3 generate-gallery.py && systemctl restart vonesse-photos`

## Security Notes
- The Samba share is only accessible on the local network
- Photos are stored in `/var/www/photos` (not in the git repo)
- The app runs as `www-data` (non-root user)
- Consider setting up fail2ban for Samba

## Troubleshooting
- **Gallery not loading**: Check Nginx logs: `journalctl -u nginx`
- **SMB not working**: Check Samba logs: `journalctl -u smbd`
- **Photos not showing**: Run `python3 generate-gallery.py` manually
- **Permission errors**: Ensure `www-data` owns the app directory: `chown -R www-data:www-data /var/www/vonesse-photos`