#!/usr/bin/env bash

if [ ! -f 'start.sh' ]; then
    echo "Usage: $0"
    echo "Run from recipe-creator-backend installation folder"
    exit 1
fi

set -eE
[ -f .venv/bin/pip ] || python3 -m venv .venv/
source .venv/bin/activate
pip3 install -r requirements.txt

escaped_path=$(pwd | sed -e 's/[\/&]/\\&/g')

echo "Writing systemd service..."
cat recipe-creator-backend.service.template | sed -e 's/%%PATH%%/'"$escaped_path"'/gm' | sudo tee /etc/systemd/system/recipe-creator-backend.service
sudo systemctl daemon-reload
echo "Enabling service..."
sudo systemctl enable recipe-creator-backend
echo "Starting service..."
sudo systemctl start recipe-creator-backend
echo "Installation complete."

