#!/bin/bash

echo "🚀 Starting Tongue Detection Server..."
echo ""

# Check if script is already running
if pgrep -f "tongue_detection_simple.py" > /dev/null; then
    echo "⚠️ Tongue detection is already running!"
    echo "   Killing old process..."
    pkill -f "tongue_detection_simple.py"
    sleep 2
fi

# Start the script
echo "📹 Starting camera and WebSocket server..."
echo "   - WebSocket: ws://localhost:8765"
echo "   - Camera window will open"
echo "   - Press 'q' in camera window to quit"
echo ""

python3 tongue_detection_simple.py

