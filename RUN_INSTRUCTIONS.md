# 🎯 How to Run Tongue Detection (FIXED)

## ⚠️ IMPORTANT: You need to run this in a **visible terminal window**, not in background!

## Step 1: Open a New Terminal Window

Open Terminal.app (or your terminal) - make sure you can see the terminal window.

## Step 2: Navigate to Project Directory

```bash
cd /Users/josekerketta/Desktop/codes/stoopid/stupid-hackathon
```

## Step 3: Start Tongue Detection Server

Run this command in the terminal (you should see it in the window):

```bash
python3 tongue_detection_simple.py
```

**Expected output:**
```
🚀 Starting MediaPipe Tongue Detection Server...
✅ WebSocket server started. Waiting for clients to connect...
🌐 Starting WebSocket server on ws://localhost:8765
✅ Using camera index 0
📹 Starting camera...
👅 Tongue detection active! Move your tongue and watch the display.
📺 Camera window should open now. Press 'q' in the window to quit.
```

**A camera window should pop up** showing your face with MediaPipe mesh overlay.

## Step 4: Keep That Terminal Open!

**DON'T close the terminal** - it needs to stay running. The camera window will also stay open.

## Step 5: Start Web Server (New Terminal)

Open a **SECOND terminal window** and run:

```bash
cd /Users/josekerkerketta/Desktop/codes/stoopid/stupid-hackathon
python3 -m http.server 8000
```

## Step 6: Open Website

Open your browser and go to:
```
http://localhost:8000/index.html
```

## ✅ What You Should See:

1. **Terminal 1**: Shows "👅 Detected: RIGHT/LEFT/CENTER" messages
2. **Camera Window**: Shows your face with green mesh and "Tongue: [POSITION]"
3. **Website**: Shows the tongue position updating in real-time with colors

## 🔍 Troubleshooting

### Camera Window Doesn't Appear

If the camera window doesn't open:
1. Check if your terminal has permission to access camera
2. Try running with explicit display:
   ```bash
   python3 tongue_detection_simple.py
   ```
3. Check System Preferences → Security & Privacy → Camera
4. Make sure Terminal has camera access

### WebSocket Connection Failed

If website shows "Disconnected":
1. Make sure `tongue_detection_simple.py` is running in Terminal 1
2. Check Terminal 1 for "✅ Client connected" message when you open the website
3. Look for errors in Terminal 1

### Position Always Shows "NEUTRAL"

1. Make sure your face is visible in the camera window
2. Check that green mesh overlay is showing on your face
3. Make sure face is well-lit
4. Try moving tongue more dramatically left/right

### Browser Console Errors

Press F12 in browser and check Console tab:
- Should see: `✅ Connected to tongue detection server`
- If you see WebSocket errors, check Terminal 1 is running

## 🛑 To Stop:

1. Press 'q' in the camera window, OR
2. Press Ctrl+C in Terminal 1
3. Then stop the web server (Ctrl+C in Terminal 2)

