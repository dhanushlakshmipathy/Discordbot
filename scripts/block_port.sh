#!/bin/bash
PORT=$1
sudo iptables -I INPUT -p tcp --dport ${PORT} -j DROP
echo "🧱 Blocked TCP port $PORT."
