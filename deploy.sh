#!/bin/bash
# Smart Garden System — Deployment Script
# Usage: ./deploy.sh <pi-ip-address>
# Example: ./deploy.sh 192.168.1.50

PI_IP=$1
PI_USER="pi"
PI_DIR="/home/pi/smart-garden-system"

if [ -z "$PI_IP" ]; then
    echo "Usage: ./deploy.sh <pi-ip-address>"
    exit 1
fi

echo "Deploying to Raspberry Pi at $PI_IP..."

# Copy project files to Pi
rsync -av --exclude='.git' --exclude='data/' --exclude='trained_models/' --exclude='.env' \
    ./ $PI_USER@$PI_IP:$PI_DIR/

# SSH into Pi and set up
ssh $PI_USER@$PI_IP << EOF
    cd $PI_DIR

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi

    # Install dependencies
    venv/bin/pip install -r requirements.txt

    # Create data directory if it doesn't exist
    mkdir -p data trained_models

    # Install and start systemd service
    sudo cp smart-garden.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable smart-garden
    sudo systemctl restart smart-garden

    echo "Deployment complete. Service status:"
    sudo systemctl status smart-garden
EOF
