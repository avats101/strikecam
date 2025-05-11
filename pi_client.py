import cv2
import socket
import json
import time
import base64
from datetime import datetime
from picamera2 import Picamera2
from ultralytics import YOLO

# Network settings
LAPTOP_IP = '10.42.0.250'  # Your laptop IP
PORT = 5000

# Detection targets
INTEREST_CLASSES = {
    "camouflage_soldier",
    "weapon",
    "military_tank",
    "military_truck",
    "military_vehicle",
    "soldier",
    "military_artillery",
    "military_aircraft",
    "military_warship"
}

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (1280, 1280)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load model
model = YOLO("model_1.pt")

def encode_frame_to_base64(frame):
    success, buffer = cv2.imencode('.jpg', frame)
    if not success:
        raise ValueError("Could not encode frame.")
    return base64.b64encode(buffer).decode('utf-8')

def send_payload(label, confidence, encoded_image):
    payload = {
        "timestamp": datetime.isoformat(),
        "object_detected": label,
        "confidence": round(confidence, 3),
        "image_base64": encoded_image
    }
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print(f"[CLIENT] Connecting to {LAPTOP_IP}:{PORT}...")
            s.connect((LAPTOP_IP, PORT))
            s.sendall(json.dumps(payload).encode())
            print(f"[CLIENT] Sent detection: {label} ({confidence:.2f})")
    except Exception as e:
        print("[CLIENT] Failed to send payload:", e)


while True:
    frame = picam2.capture_array()
    results = model(frame)[0]

    for box in results.boxes:
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        label = model.names[cls_id]

        if label in INTEREST_CLASSES and confidence > 0.70:
            try:
                encoded_image = encode_frame_to_base64(frame)
                send_payload(label, confidence, encoded_image)
            except Exception as e:
                print("[CLIENT] Error preparing/sending image:", e)

    # Annotate and show
    annotated_frame = results.plot()
    fps = 1000 / results.speed['inference']
    cv2.putText(annotated_frame, f'FPS: {fps:.1f}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Camera", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
