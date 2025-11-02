import cv2
import mediapipe as mp
import asyncio
import websockets
import json
import threading
import time

print("🚀 Starting MediaPipe Head Tilt Detection Server...")

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# WebSocket server for broadcasting tongue positions
connected_clients = set()
position_queue = None
websocket_loop = None

async def register_client(websocket):
    connected_clients.add(websocket)
    print(f"✅ Client connected. Total clients: {len(connected_clients)}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"❌ Client disconnected. Total clients: {len(connected_clients)}")

async def broadcast_head_tilt(position):
    """Broadcast head tilt position to all connected clients"""
    global connected_clients
    if connected_clients:
        message = json.dumps({"head_tilt": position})
        disconnected = set()
        for client in connected_clients.copy():  # Use copy to avoid modification during iteration
            try:
                await client.send(message)
            except (websockets.exceptions.ConnectionClosed, Exception) as e:
                disconnected.add(client)
        connected_clients -= disconnected

async def broadcast_worker():
    """Worker that broadcasts messages from queue"""
    while True:
        position = await position_queue.get()
        await broadcast_head_tilt(position)
        position_queue.task_done()

async def websocket_server():
    """Start WebSocket server on port 8765"""
    global position_queue
    print("🌐 Starting WebSocket server on ws://localhost:8765")
    position_queue = asyncio.Queue()
    # Start broadcast worker
    asyncio.create_task(broadcast_worker())
    async with websockets.serve(register_client, "localhost", 8765):
        await asyncio.Future()  # run forever

def start_websocket_server():
    """Start WebSocket server in a separate thread"""
    global websocket_loop
    websocket_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(websocket_loop)
    websocket_loop.run_until_complete(websocket_server())

def detect_head_tilt(landmarks, image_width, image_height):
    """
    Detect head tilt/rotation based on MediaPipe landmarks.
    Uses key facial landmarks to calculate head rotation angle.
    """
    try:
        # Key landmarks for head pose estimation
        # Left and right eye outer corners
        left_eye_outer = landmarks.landmark[33]   # Left eye outer corner
        right_eye_outer = landmarks.landmark[263]  # Right eye outer corner
        
        # Left and right face edge points
        left_face = landmarks.landmark[234]  # Left side of face
        right_face = landmarks.landmark[454]  # Right side of face
        
        # Nose tip
        nose_tip = landmarks.landmark[4]
        
        # Calculate horizontal distance between eye corners (should be level if head is straight)
        eye_distance = abs(left_eye_outer.x - right_eye_outer.x) * image_width
        
        # Calculate vertical difference between eye corners (indicates tilt)
        eye_vertical_diff = (right_eye_outer.y - left_eye_outer.y) * image_height
        
        # Calculate tilt angle based on eye level difference
        # Positive = right eye lower (head tilted right)
        # Negative = left eye lower (head tilted left)
        tilt_ratio = eye_vertical_diff / eye_distance if eye_distance > 0 else 0
        
        # Threshold for detection (adjust sensitivity here)
        # Higher threshold = need more tilt to trigger
        tilt_threshold = 0.05  # 5% of eye distance
        
        if tilt_ratio > tilt_threshold:
            # Head tilted right (right eye is lower)
            return "right"
        elif tilt_ratio < -tilt_threshold:
            # Head tilted left (left eye is lower)
            return "left"
        else:
            # Head is relatively straight
            return "center"
            
    except Exception as e:
        print(f"Error detecting head tilt: {e}")
        return "center"

# Start WebSocket server in background thread
websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
websocket_thread.start()
print("✅ WebSocket server started. Waiting for clients to connect...")
time.sleep(1)

# Initialize camera
def open_camera():
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ Using camera index {i}")
            return cap
    raise RuntimeError("❌ No working camera found!")

cap = open_camera()

# Initialize MediaPipe Face Mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,  # This includes mouth and eye landmarks
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

print("📹 Starting camera...")
print("👤 Head tilt detection active! Tilt your head left/right to control video.")
print("📺 Camera window should open now. Press 'q' in the window to quit.")
print("")

last_position = None
last_broadcast_time = 0
broadcast_cooldown = 0.3  # Broadcast max once per 300ms
frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to read frame from camera")
            time.sleep(0.1)
            continue
        
        frame_count += 1
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        image_height, image_width, _ = frame.shape
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        
        # Draw face mesh
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                # Draw face mesh
                mp_drawing.draw_landmarks(
                    frame,
                    face_landmarks,
                    mp_face_mesh.FACEMESH_CONTOURS,
                    None,
                    mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                )
                
                # Detect head tilt
                head_tilt = detect_head_tilt(face_landmarks, image_width, image_height)
                
                # Display on frame with color coding
                color = (0, 255, 0)  # Green for center
                if head_tilt == "right":
                    color = (255, 0, 0)  # Blue for right
                elif head_tilt == "left":
                    color = (255, 0, 255)  # Magenta for left
                
                cv2.putText(frame, f"Head: {head_tilt.upper()}", 
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
                
                # Also draw direction indicator
                if head_tilt == "right":
                    cv2.putText(frame, "->", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                elif head_tilt == "left":
                    cv2.putText(frame, "<-", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                
                # Broadcast position - always send current position, not just on change
                current_time = time.time()
                # Always broadcast, but throttle frequency
                if (current_time - last_broadcast_time) > broadcast_cooldown:
                    last_broadcast_time = current_time
                    
                    # Update last_position for console logging
                    if head_tilt != last_position:
                        last_position = head_tilt
                        print(f"👤 Head Tilt: {head_tilt.upper()} (Broadcasting to {len(connected_clients)} clients)")
                    
                    # Always broadcast current position to keep display updated
                    if websocket_loop and position_queue:
                        try:
                            asyncio.run_coroutine_threadsafe(position_queue.put(head_tilt), websocket_loop)
                        except Exception as e:
                            print(f"⚠️ Error broadcasting: {e}")
        else:
            # No face detected
            if frame_count % 60 == 0:  # Print every 60 frames
                cv2.putText(frame, "No face detected", 
                           (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Show frame
        cv2.imshow('MediaPipe Head Tilt Detection - Press Q to quit', frame)
        
        # Check for quit
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("\n🛑 Quit key pressed. Shutting down...")
            break
            
except KeyboardInterrupt:
    print("\n🛑 Interrupted by user. Shutting down...")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    cap.release()
    cv2.destroyAllWindows()
    print("👋 Shutting down...")

