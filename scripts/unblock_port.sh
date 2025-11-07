#!/bin/bash

# Usage: ./manage_port.sh 5000
PORT="$1"

if [ -z "$PORT" ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

# Allow TCP port via UFW
sudo ufw allow "${PORT}/tcp" && \
echo "✅ Allowed TCP port ${PORT} via UFW." || \
{ echo "❌ Failed to allow port ${PORT}. Check sudo privileges and UFW status."; exit 2; }

# Optional: show the rule we just added
sudo ufw status numbered | grep "${PORT}/tcp" || true
