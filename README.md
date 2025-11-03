# ScreamStream

YouTube immersiveness (and laziness) to the max

## Installation

1. **Clone or download this repository**

2. **Install Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## How to Run

### Option 1: Quick Start (Recommended)

Use the automated setup script that starts everything in the background:

```bash
cd run
./reset_and_test.sh
```

This script will:
- Stop any existing servers
- Start the head tilt detection server (port 8765)
- Start the web server (port 8000)
- Display server PIDs and log locations

Then open your browser to: **http://localhost:8000/index.html**

## Usage

1. **Open the application**: Navigate to `http://localhost:8000/index.html` in your browser

2. **Control the video**:
   - **Voice Volume**: Speak louder to increase YouTube video volume
   - **Head Tilt**: 
     - Tilt head **LEFT** ← to skip backward
     - Tilt head **RIGHT** → to skip forward
   - **Normal position**: Keep head centered for normal playback

4. **Load a different video**: Enter a YouTube URL in the input field and click "Load Video"

5. **Camera window**: You'll see a window showing your face with the face mesh overlay and current head position detection


**Port already in use:**
- Run `./run/stop_servers.sh` to kill existing processes
- Or manually kill processes on ports 8000 and 8765


## Technical Details

- **Head Detection**: Uses MediaPipe Face Mesh for real-time head pose estimation
- **WebSocket**: Communication between Python backend and web frontend
- **Voice Analysis**: Web Audio API for real-time microphone input analysis
