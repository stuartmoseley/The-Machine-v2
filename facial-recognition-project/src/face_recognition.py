from deepface import DeepFace
import cv2
import hashlib
import json
import os
from secure_storage import encrypt_data, decrypt_data

FACE_DATA_FILE = "facebase/face_data.enc"

def generate_face_id(face_img):
    face_hash = hashlib.md5(face_img).hexdigest()[:5]
    return face_hash

def load_face_data():
    if os.path.exists(FACE_DATA_FILE):
        decrypted_data = decrypt_data(FACE_DATA_FILE)
        return json.loads(decrypted_data)
    return {}

def save_face_data(face_data):
    encrypted_data = json.dumps(face_data)
    encrypt_data(encrypted_data, FACE_DATA_FILE)

def recognize_faces(frame, face_region, source):
    x, y, w, h = face_region
    face_img = frame[y:y+h, x:x+w]
    face_id = generate_face_id(face_img.tobytes())
    face_data = load_face_data()

    try:
        # Recognize face
        result = DeepFace.find(face_img, db_path="facebase/known_faces", enforce_detection=False)
        if len(result) > 0:
            cv2.putText(frame, f"ID: {face_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            face_status = "Known"
        else:
            cv2.putText(frame, f"ID: {face_id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            face_status = "Unknown"
        
        # Predict emotion, age, and gender
        analysis = DeepFace.analyze(face_img, actions=['emotion', 'age', 'gender'], enforce_detection=False)
        emotion = analysis['dominant_emotion']
        age = analysis['age']
        gender = analysis['gender']
        
        cv2.putText(frame, f"Emotion: {emotion}", (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Age: {age}", (x, y + h + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, f"Gender: {gender}", (x, y + h + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Store face information
        face_data[face_id] = {
            "emotion": emotion,
            "age": age,
            "gender": gender,
            "status": face_status
        }
        save_face_data(face_data)
        
        return face_status
    except Exception as e:
        print(f"Error recognizing face from {source}: {e}")
        return "Error"

def search_face_by_id(face_id, frame, face_region):
    x, y, w, h = face_region
    face_img = frame[y:y+h, x:x+w]
    current_face_id = generate_face_id(face_img.tobytes())
    return current_face_id == face_id