# 🎯 Simple MediaPipe Tongue Detection

This is a **NO-TRAINING** version that uses MediaPipe's face mesh landmarks to detect tongue position in real-time!

## ✨ Features

- **No training required** - Works immediately with MediaPipe
- **Real-time detection** - Detects: `LEFT`, `RIGHT`, `CENTER`, `NEUTRAL`
- **Visual display** - Shows position on the website with color coding
- **WebSocket communication** - Sends updates to browser in real-time

## 🚀 Quick Start

### Option 1: Run Everything Automatically

```bash
# Make scripts executable (if not already)
chmod +x run_tongue_detection.sh start_all.sh

# Run the tongue detection server
./run_tongue_detection.sh
```

Then in a **NEW terminal**:
```bash
# Start web server
python3 -m http.server 8000
```

### Option 2: Manual Steps

**Terminal 1 - Tongue Detection:**
```bash
python3 tongue_detection_simple.py
```

**Terminal 2 - Web Server:**
```bash
python3 -m http.server 8000
```

**Browser:**
```
http://localhost:8000/index.html
```

## 📋 How It Works

1. **MediaPipe Face Mesh** detects your face landmarks (468 points)
2. **Tongue detection algorithm** analyzes mouth landmarks to determine position
3. **WebSocket server** broadcasts position to browser (port 8765)
4. **Website displays** the position in real-time with color coding:
   - 🔵 `RIGHT` = Blue
   - 🟣 `LEFT` = Purple  
   - 🟡 `CENTER` = Yellow
   - ⚪ `NEUTRAL` = Gray

## 🎨 Detection Logic

The script uses these MediaPipe landmarks:
- Mouth corners (landmarks 61, 291)
- Lower lip (landmark 18)
- Inner mouth points
- Relative positions to determine tongue direction

## ⚙️ Configuration

### Adjust Sensitivity
Edit `tongue_detection_simple.py`:
- `broadcast_cooldown = 0.3` - How often to send updates (seconds)
- Threshold values in `detect_tongue_position()` function

### Camera Settings
The script automatically finds your camera. If it doesn't work:
- Change camera index in `open_camera()` function (0, 1, or 2)

## 🐛 Troubleshooting

### Camera Not Found
```bash
# Check available cameras
python3 -c "import cv2; [print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}') for i in range(5)]"
```

### WebSocket Connection Failed
- Make sure `tongue_detection_simple.py` is running
- Check that port 8765 is not blocked
- Look for "✅ WebSocket server started" in terminal

### Position Always Shows "NEUTRAL"
- Make sure your face is well-lit
- Position face clearly in camera view
- Check that MediaPipe is detecting face (green mesh should appear)

### Website Not Showing Position
- Open browser console (F12)
- Check for WebSocket connection errors
- Make sure you're using `http://localhost:8000` not `file://`

## 📝 Differences from ML Version

| Feature | ML Version (`tongue.py`) | Simple Version (`tongue_detection_simple.py`) |
|---------|-------------------------|-----------------------------------------------|
| Training | ✅ Required | ❌ None needed |
| Accuracy | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐ Good |
| Setup Time | ~10-15 minutes | Instant |
| Detection Method | Machine Learning (SVM) | MediaPipe landmarks |
| Best For | Production use | Quick testing/demos |

## 🎮 Control YouTube

The detected position also controls YouTube:
- `RIGHT` → ⏩ Forward 10 seconds
- `LEFT` → ⏪ Backward 10 seconds
- `CENTER` → ⏯️ Play/Pause
- `NEUTRAL` → No action

## 🔧 Customization

Want to improve detection? Edit the `detect_tongue_position()` function:
- Adjust threshold values
- Add more landmark checks
- Implement smoothing/averaging
- Add gesture recognition

## 📚 MediaPipe Documentation

- [Face Mesh Guide](https://google.github.io/mediapipe/solutions/face_mesh.html)
- [Landmark Index Map](https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png)

