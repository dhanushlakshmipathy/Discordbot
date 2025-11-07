#!/bin/bash
PORT=$1
PID=$(sudo lsof -t -i:$PORT)
if [ -z "$PID" ]; then
  echo "No process found on port $PORT."
else
  sudo kill -9 $PID
  echo "✅ Closed port $PORT (PID $PID)."
fi
