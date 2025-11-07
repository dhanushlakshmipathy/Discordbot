#!/bin/bash
PORT=$1
sudo iptables -I ufw-before-input -p tcp --dport "$PORT" -j DROP;
sudo netfilter-persistent save
echo "🧱 Blocked TCP port $PORT."
