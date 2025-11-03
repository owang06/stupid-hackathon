#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting ScreamStream Application..."
echo ""

# Terminal 1: Start tongue detection
echo "📹 Starting tongue detection server..."
osascript -e 'tell app "Terminal" to do script "cd '"$PROJECT_DIR"' && python3 tongue_detection_simple.py"'

# Wait a bit for WebSocket server to start
sleep 2

# Terminal 2: Start web server
echo "🌐 Starting web server..."
osascript -e 'tell app "Terminal" to do script "cd '"$PROJECT_DIR"' && python3 -m http.server 8000"'

# Wait a bit
sleep 1

echo ""
echo "✅ All servers started!"
echo ""
echo "📹 Terminal 1: Tongue detection (WebSocket on port 8765)"
echo "🌐 Terminal 2: Web server (HTTP on port 8000)"
echo ""
echo "🌍 Open your browser to: http://localhost:8000/index.html"
echo ""
echo "Press Ctrl+C to stop this script (servers will keep running in their terminals)"

