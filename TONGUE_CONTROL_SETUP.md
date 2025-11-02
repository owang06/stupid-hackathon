# Tongue Control Setup

This guide explains how to set up tongue detection to control the YouTube video player in `index.html`.

## Prerequisites

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Train the tongue detection model (first time only):
   - Run `python tongue.py`
   - When prompted, enter `y` to collect training data
   - Follow the prompts to collect data for: `neutral`, `center`, `left`, and `right` tongue positions
   - Press `q` when done with each position
   - The model will be saved to `tongue_model.pkl`

## Usage

1. **Start the tongue detection server:**
   ```bash
   python tongue.py
   ```
   - The WebSocket server will start on `ws://localhost:8765`
   - Make sure your face is visible to the camera
   - You'll see a window showing the detected tongue position

2. **Open the web app:**
   - Open `index.html` in your browser (via a local server, e.g., `python3 -m http.server 8000`)
   - The page will automatically connect to the tongue detection server

3. **Control the video:**
   - **Tongue Right** → Fast forward 10 seconds (like pressing `L` key)
   - **Tongue Left** → Rewind 10 seconds (like pressing `J` key)  
   - **Tongue Center** → Toggle play/pause (like pressing `K` key)
   - **Neutral** → No action

## Notes

- The tongue detection has a 1-second cooldown between actions to prevent spam
- Make sure the camera is positioned so your face is clearly visible
- The WebSocket connection will automatically reconnect if it drops
- Check the browser console for connection status and action logs

## Troubleshooting

- **"Could not connect to tongue detection server"**: Make sure `tongue.py` is running
- **No tongue detection**: Check that your face is visible and well-lit
- **Video controls not working**: Make sure the YouTube iframe has `enablejsapi=1` in the URL

