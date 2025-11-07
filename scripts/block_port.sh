#!/bin/bash
PORT=$1
sudo ufw deny $PORT/tcp
echo "🧱 Blocked TCP port $PORT via UFW."
