#!/bin/bash
PORT=$1
sudo iptables -D INPUT -p tcp --dport $PORT -j DROP
echo "🧱 UnBlocked TCP port $PORT."
