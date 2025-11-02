# 🚀 Quick Start Guide

## Step 1: Install Python Dependencies

```bash
pip install opencv-python mediapipe scikit-learn websockets numpy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

## Step 2: Train the Model (First Time Only)

Run the script and collect training data:
```bash
python tongue.py
```

When prompted:
- Type `y` and press Enter to collect training data
- For each position (`neutral`, `center`, `left`, `right`):
  - Position your tongue as instructed
  - Press `q` when done with that position
  - Repeat for all 4 positions
- The model will train and save to `tongue_model.pkl`

## Step 3: Run the Detection Server

After training (or if you already have `tongue_model.pkl`):

```bash
python tongue.py
```

When prompted:
- Type `n` and press Enter (skip training)
- A camera window will open showing your face
- The WebSocket server starts on `ws://localhost:8765`
- You'll see "Tongue: [position]" text on the camera feed

**Keep this terminal window open!**

## Step 4: Start the Web Server

Open a **NEW terminal window** and run:

```bash
# Option 1: Python 3
python3 -m http.server 8000

# Option 2: Python 2
python -m http.server 8000

# Option 3: Node.js (if you have it)
npx http-server
```

## Step 5: Open the Web App

Open your browser and go to:
```
http://localhost:8000/index.html
```

**Important**: Don't open `index.html` directly from the file system (`file://`) - it won't work!

## Step 6: Allow Camera/Microphone Access

When the page loads:
- Click "Allow" when the browser asks for camera/microphone permissions
- You should see your facecam appear
- Check the browser console (F12) - you should see "✅ Connected to tongue detection server"

## Step 7: Control the Video! 🎮

Move your tongue to control the YouTube video:
- 👅 **Tongue Right** → Fast forward 10 seconds
- 👅 **Tongue Left** → Rewind 10 seconds
- 👅 **Tongue Center** → Play/Pause
- 👅 **Neutral** → No action

## Troubleshooting

### ❌ "No working camera found!"
- Make sure your camera is connected and not being used by another app
- Try closing other apps that might be using the camera

### ❌ "Could not connect to tongue detection server"
- Make sure `tongue.py` is running (check the terminal)
- Make sure you typed `n` to skip training and start detection
- Check that port 8765 is not blocked by firewall

### ❌ Video controls don't work
- Open browser console (F12) and check for errors
- Make sure the YouTube video is loaded
- Try refreshing the page

### ❌ "Module not found" errors
- Install missing packages: `pip install [package-name]`
- Or reinstall all: `pip install -r requirements.txt`

### ❌ WebSocket connection issues
- Make sure `tongue.py` is running BEFORE opening the web page
- Check that both are on the same computer (localhost)
- Try restarting both the Python script and the web server

## That's It! 🎉

You should now be able to control YouTube videos with your tongue!

