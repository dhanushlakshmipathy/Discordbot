#!/bin/bash
PORT=$1
sudo ufw delete deny $PORT/tcp
echo "🪚 Unblocked TCP port $PORT via UFW."
