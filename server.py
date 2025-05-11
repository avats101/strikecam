import socket
import json
import base64
import os
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5000
IMAGE_DIR = "received_images"
LOG_FILE = "detection_log.jsonl"

os.makedirs(IMAGE_DIR, exist_ok=True)

def save_image(base64_string, timestamp, label):
    try:
        image_data = base64.b64decode(base64_string)
        safe_timestamp = timestamp.replace(":", "_").replace(".", "_")
        filename = f"{IMAGE_DIR}/received_{safe_timestamp}_{label}.jpg"
        with open(filename, "wb") as f:
            f.write(image_data)
        print(f"[SERVER] Image saved to: {filename}")
    except Exception as e:
        print(f"[SERVER] Error saving image: {e}")

def append_log(payload):
    try:
        with open(LOG_FILE, "a") as log_file:
            json.dump(payload, log_file)
            log_file.write("\n")
        print(f"[SERVER] Logged detection to {LOG_FILE}")
    except Exception as e:
        print(f"[SERVER] Error logging payload: {e}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[SERVER] Listening on port {PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            # print(f"[SERVER] Connected by {addr}")
            print(f"[SERVER] Connected by 10.42.0.1")
            try:
                chunks = []
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    chunks.append(chunk)
                data = b"".join(chunks)

                if data:
                    payload = json.loads(data.decode())
                    print(f"[SERVER] Detection: {payload['object_detected']} ({payload['confidence']}) at {payload['timestamp']}")
                    save_image(payload["image_base64"], payload["timestamp"], payload["object_detected"])
                    append_log(payload)
            except Exception as e:
                print(f"[SERVER] Error processing data: {e}")
