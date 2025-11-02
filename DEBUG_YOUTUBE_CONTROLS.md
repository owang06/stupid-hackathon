# Debugging YouTube Controls

## What I Fixed:

1. **Changed postMessage origin**: From `'*'` to `'https://www.youtube.com'` (more secure, sometimes required)
2. **Added time tracking**: Periodically requests current time from YouTube player
3. **Added origin parameter**: Added `&origin=http://localhost:8000` to YouTube embed URL
4. **Better logging**: Added console logs to see what's happening
5. **Improved error handling**: Better checks for iframe readiness

## How to Debug:

1. **Open Browser Console** (F12)
2. **Check for these logs:**
   - `✅ Connected to tongue detection server` - WebSocket connected
   - `✅ YouTube player ready` - YouTube iframe is ready
   - `👅 Tongue detected: right` - Tongue position received
   - `🎮 Executing action for: right` - About to send command
   - `⏩ Forward 10s (current: X.Xs, seeking to: Y.Ys)` - Command sent

3. **Check for errors:**
   - `⚠️ YouTube iframe not found` - Iframe not loaded
   - WebSocket connection errors
   - CORS errors in console

## Possible Issues & Solutions:

### Issue 1: "YouTube iframe not found"
**Solution**: Make sure the iframe is fully loaded before trying to control it.

### Issue 2: Commands sent but nothing happens
**Possible causes:**
- YouTube video hasn't started playing yet
- Video is paused and needs to be played first
- The video might not allow embedding/controls

**Solution**: 
- Manually play the video once
- Try clicking play/pause button in YouTube player first
- Try a different video ID

### Issue 3: `currentVideoTime` stays at 0
**Solution**: 
- The periodic time request should fix this
- Wait a few seconds after page loads
- Check console for time updates

### Issue 4: CORS/Security errors
**Solution**:
- Make sure you're using `http://localhost:8000` not `file://`
- The origin parameter in the embed URL should match your server URL

### Issue 5: YouTube IFrame API not responding
**Solution**:
- Some videos don't allow embedding
- Try a different video ID
- Make sure video has `enablejsapi=1` in URL

## Test Commands Manually:

Open browser console and try these manually:

```javascript
// Test if iframe exists
const iframe = document.getElementById('youtubeFrame');
console.log(iframe);

// Test postMessage manually
iframe.contentWindow.postMessage(JSON.stringify({
    event: 'command',
    func: 'playVideo'
}), 'https://www.youtube.com');

// Test seek
iframe.contentWindow.postMessage(JSON.stringify({
    event: 'command',
    func: 'seekTo',
    args: [30, true]  // Seek to 30 seconds
}), 'https://www.youtube.com');
```

If these work manually but not from tongue detection, the issue is in the WebSocket → command flow.

