import cv2
import mediapipe as mp
import numpy as np
from sklearn.svm import SVC
import pickle
import asyncio
import websockets
import json
import threading

print("Script started")

# WebSocket server for broadcasting tongue positions
connected_clients = set()
position_queue = None
websocket_loop = None

async def register_client(websocket):
    connected_clients.add(websocket)
    print(f"Client connected. Total clients: {len(connected_clients)}")
    try:
        await websocket.wait_closed()
    finally:
        connected_clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(connected_clients)}")

async def broadcast_worker():
    """Worker that broadcasts messages from queue"""
    while True:
        position = await position_queue.get()
        if connected_clients:
            message = json.dumps({"tongue_position": position})
            disconnected = set()
            for client in connected_clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.add(client)
            connected_clients -= disconnected
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

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Collect data
data = []
labels = []

def capture_data(label):
    def open_camera():
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"✅ Using camera index {i}")
                return cap
        raise RuntimeError("❌ No working camera found!")

    # then use it like this
    cap = open_camera()

    print(f"Collecting data for '{label}'. Press 'q' when done.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb)
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0]
            coords = np.array([[lm.x, lm.y, lm.z] for lm in landmarks.landmark]).flatten()
            data.append(coords)
            labels.append(label)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# --- 1️⃣ ask before collecting data ---
choice = input("Collect new training data? (y/n): ").strip().lower()

if choice == "y":
    for lbl in ["neutral", "center", "left", "right"]:
        capture_data(lbl)

    # --- 2️⃣ train & save ---
    if len(data) == 0:
        print("❌ No data collected! Make sure your face is visible before pressing 'q'.")
        exit()

    clf = SVC(kernel='linear')
    clf.fit(data, labels)

    with open("tongue_model.pkl", "wb") as f:
        pickle.dump(clf, f)
    print("✅ Model saved to tongue_model.pkl")

# --- 3️⃣ load model for detection ---
with open("tongue_model.pkl", "rb") as f:
    clf = pickle.load(f)
print("Model loaded. Starting real-time detection...")

# --- 4️⃣ live detection loop ---
def open_camera():
    for i in range(3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ Using camera index {i}")
            return cap
    raise RuntimeError("❌ No working camera found!")

# Start WebSocket server in background thread
websocket_thread = threading.Thread(target=start_websocket_server, daemon=True)
websocket_thread.start()
print("✅ WebSocket server started. Waiting for clients to connect...")

# Wait a moment for server to start
import time
time.sleep(1)

# then use it like this
cap = open_camera()

last_position = None
last_broadcast_time = 0
broadcast_cooldown = 0.5  # Broadcast max once per 500ms to avoid spam

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if results.multi_face_landmarks:
        coords = np.array([[lm.x, lm.y, lm.z] for lm in results.multi_face_landmarks[0].landmark]).flatten()
        pred = clf.predict([coords])[0]
        
        # Only broadcast if position changed or cooldown expired
        current_time = time.time()
        if pred != last_position or (current_time - last_broadcast_time) > broadcast_cooldown:
            last_position = pred
            last_broadcast_time = current_time
            
            # Add to queue for async broadcasting
            if websocket_loop and position_queue:
                asyncio.run_coroutine_threadsafe(position_queue.put(pred), websocket_loop)
        
        cv2.putText(frame, f"Tongue: {pred}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()