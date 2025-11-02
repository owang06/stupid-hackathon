#!/bin/bash

echo "🛑 Stopping all servers..."

pkill -f "tongue_detection" 2>/dev/null
pkill -f "http.server" 2>/dev/null
lsof -ti:8765,8000 2>/dev/null | xargs kill -9 2>/dev/null

sleep 1

if lsof -ti:8765,8000 2>/dev/null; then
    echo "⚠️ Some processes still running. Force killing..."
    lsof -ti:8765,8000 2>/dev/null | xargs kill -9 2>/dev/null
    sleep 1
fi

echo "✅ All servers stopped"

