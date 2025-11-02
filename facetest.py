import cv2
import mediapipe as mp
import numpy as np
from sklearn.svm import SVC
import pickle

print("Script started")

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

# then use it like this
cap = open_camera()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if results.multi_face_landmarks:
        coords = np.array([[lm.x, lm.y, lm.z] for lm in results.multi_face_landmarks[0].landmark]).flatten()
        pred = clf.predict([coords])[0]
        cv2.putText(frame, f"Tongue: {pred}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
