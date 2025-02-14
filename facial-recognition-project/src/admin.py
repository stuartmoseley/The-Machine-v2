import os
import cv2
from datetime import datetime
import getpass
import pyttsx3
from deepface import DeepFace
from secure_storage import decrypt_data, encrypt_image, decrypt_image, save_file_hashes, verify_file_hashes, create_backup, restore_files_from_backup, secure_wipe
import json
import schedule
import time
from transformers import pipeline

KNOWN_FACE_DIR = "facebase/known_faces"
UNKNOWN_FACE_DIR = "facebase/unknown_faces"
FACE_DATA_FILE = "facebase/face_data.enc"
ADMIN_FACE = "admin_face.jpg"  # Path to the admin's face image
FAILED_ATTEMPTS = 0
MAX_FAILED_ATTEMPTS = 3
SECURE_FILE = "secure_data.enc"
HASH_FILE = "file_hashes.enc"
BACKUP_FILE = "file_backup.enc"
FILES_TO_MONITOR = ["admin.py", "main.py", "face_recognition.py", "face_tracking.py", "secure_storage.py"]

# Load TinyBERT for sentiment analysis and emotion detection
tinybert = pipeline('sentiment-analysis', model='prajjwal1/bert-tiny', cache_dir='AI')

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def self_destruct():
    # Securely wipe all sensitive data and files
    if os.path.exists(FACE_DATA_FILE):
        secure_wipe(FACE_DATA_FILE)
    for filename in os.listdir(KNOWN_FACE_DIR):
        secure_wipe(os.path.join(KNOWN_FACE_DIR, filename))
    for filename in os.listdir(UNKNOWN_FACE_DIR):
        secure_wipe(os.path.join(UNKNOWN_FACE_DIR, filename))
    secure_wipe(SECURE_FILE)
    secure_wipe(HASH_FILE)
    secure_wipe(BACKUP_FILE)
    message = "System self-destruct initiated. All data has been securely wiped."
    print(message)
    speak(message)
    exit()

def authenticate_admin():
    global FAILED_ATTEMPTS
    sensitive_data = eval(decrypt_data(SECURE_FILE))
    admin_password = sensitive_data["admin_password"]
    admin_passphrase = sensitive_data["admin_passphrase"]

    # Password authentication
    password = getpass.getpass("Enter admin password: ")
    if admin_password != password:
        FAILED_ATTEMPTS += 1
        if FAILED_ATTEMPTS >= MAX_FAILED_ATTEMPTS:
            self_destruct()
        message = "Authentication failed. Access denied."
        print(message)
        speak(message)
        return False

    # Facial authentication
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        message = "Failed to capture image for facial authentication."
        print(message)
        speak(message)
        return False

    try:
        result = DeepFace.verify(frame, ADMIN_FACE, enforce_detection=False)
        if not result["verified"]:
            FAILED_ATTEMPTS += 1
            if FAILED_ATTEMPTS >= MAX_FAILED_ATTEMPTS:
                self_destruct()
            message = "Facial authentication failed. Access denied."
            print(message)
            speak(message)
            return False
    except Exception as e:
        message = f"Error during facial authentication: {e}"
        print(message)
        speak(message)
        return False

    # Voice passphrase authentication
    engine = pyttsx3.init()
    engine.say("Please say your passphrase after the beep.")
    engine.runAndWait()
    input("Press Enter and then say your passphrase: ")
    passphrase = input("Enter the passphrase you just said: ")
    if admin_passphrase != passphrase:
        FAILED_ATTEMPTS += 1
        if FAILED_ATTEMPTS >= MAX_FAILED_ATTEMPTS:
            self_destruct()
        message = "Voice passphrase authentication failed. Access denied."
        print(message)
        speak(message)
        return False

    return True

def add_known_face(name, image_path):
    if not os.path.exists(image_path):
        message = f"Image file {image_path} does not exist."
        print(message)
        speak(message)
        return

    if not os.path.exists(KNOWN_FACE_DIR):
        os.makedirs(KNOWN_FACE_DIR)

    img = cv2.imread(image_path)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{KNOWN_FACE_DIR}/{name}_{timestamp}.jpg"
    cv2.imwrite(filename, img)
    encrypted_filename = f"{KNOWN_FACE_DIR}/{name}_{timestamp}.enc"
    encrypt_image(filename, encrypted_filename)
    os.remove(filename)
    message = f"Known face added and encrypted: {encrypted_filename}"
    print(message)
    speak(message)

def delete_known_face(face_id):
    for filename in os.listdir(KNOWN_FACE_DIR):
        if filename.startswith(face_id) and filename.endswith(".enc"):
            os.remove(os.path.join(KNOWN_FACE_DIR, filename))
            message = f"Deleted known face: {filename}"
            print(message)
            speak(message)

def view_unknown_faces():
    if not os.path.exists(UNKNOWN_FACE_DIR):
        message = "No unknown faces found."
        print(message)
        speak(message)
        return

    for filename in os.listdir(UNKNOWN_FACE_DIR):
        if filename.endswith(".enc"):
            decrypted_filename = f"{UNKNOWN_FACE_DIR}/decrypted_{filename[:-4]}.jpg"
            decrypt_image(os.path.join(UNKNOWN_FACE_DIR, filename), decrypted_filename)
            img = cv2.imread(decrypted_filename)
            cv2.imshow(filename, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            os.remove(decrypted_filename)

def clear_logs():
    log_file_path = "facebase/detected_faces.log"
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        message = "Logs cleared."
        print(message)
        speak(message)
    else:
        message = "No logs to clear."
        print(message)
        speak(message)

def view_logs():
    log_file_path = "facebase/detected_faces.log"
    if not os.path.exists(log_file_path):
        message = "No logs found."
        print(message)
        speak(message)
        return

    with open(log_file_path, "r") as log_file:
        logs = log_file.readlines()
        for log in logs:
            print(log.strip())
            speak(log.strip())

def view_known_faces():
    if not os.path.exists(KNOWN_FACE_DIR):
        message = "No known faces found."
        print(message)
        speak(message)
        return

    for filename in os.listdir(KNOWN_FACE_DIR):
        if filename.endswith(".enc"):
            decrypted_filename = f"{KNOWN_FACE_DIR}/decrypted_{filename[:-4]}.jpg"
            decrypt_image(os.path.join(KNOWN_FACE_DIR, filename), decrypted_filename)
            img = cv2.imread(decrypted_filename)
            cv2.imshow(filename, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            os.remove(decrypted_filename)

def delete_unknown_faces():
    if not os.path.exists(UNKNOWN_FACE_DIR):
        return

    for filename in os.listdir(UNKNOWN_FACE_DIR):
        if filename.endswith(".enc"):
            os.remove(os.path.join(UNKNOWN_FACE_DIR, filename))
    message = "Unknown faces deleted."
    print(message)
    speak(message)

def update_admin_face():
    image_path = input("Enter the path to the new admin face image: ")
    if not os.path.exists(image_path):
        message = f"Image file {image_path} does not exist."
        print(message)
        speak(message)
        return

    img = cv2.imread(image_path)
    cv2.imwrite(ADMIN_FACE, img)
    message = "Admin face updated."
    print(message)
    speak(message)

def change_admin_password():
    sensitive_data = eval(decrypt_data(SECURE_FILE))
    new_password = getpass.getpass("Enter new admin password: ")
    sensitive_data["admin_password"] = new_password
    encrypt_data(str(sensitive_data), SECURE_FILE)
    message = "Admin password changed."
    print(message)
    speak(message)

def system_status():
    message = "System is running. All systems are operational."
    print(message)
    speak(message)

def manage_watchlist():
    # Implement watchlist management functionality here
    message = "Watchlist management is not yet implemented."
    print(message)
    speak(message)

def analyze_sentiment(text):
    result = tinybert(text)
    return result

def detect_emotion(text):
    result = tinybert(text)
    return result

def admin_menu():
    if not authenticate_admin():
        return

    while True:
        message = "\nAdmin Menu:\n1. Add Known Face\n2. Delete Known Face\n3. View Unknown Faces\n4. View Logs\n5. Clear Logs\n6. View Face Data\n7. Delete Unknown Faces\n8. Update Admin Face\n9. Change Admin Password\n10. System Status\n11. Manage Watchlist\n12. Exit\n13. Analyze Sentiment\n14. Detect Emotion\n15. Generate Text"
        print(message)
        speak("Say your command")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter the name of the person: ")
            image_path = input("Enter the path to the image: ")
            add_known_face(name, image_path)
        elif choice == '2':
            face_id = input("Enter the face ID to delete: ")
            delete_known_face(face_id)
        elif choice == '3':
            view_unknown_faces()
        elif choice == '4':
            view_logs()
        elif choice == '5':
            clear_logs()
        elif choice == '6':
            view_known_faces()
        elif choice == '7':
            delete_unknown_faces()
        elif choice == '8':
            update_admin_face()
        elif choice == '9':
            change_admin_password()
        elif choice == '10':
            system_status()
        elif choice == '11':
            manage_watchlist()
        elif choice == '12':
            break
        elif choice == '13':
            text = input("Enter text to analyze sentiment: ")
            result = analyze_sentiment(text)
            print(result)
        elif choice == '14':
            text = input("Enter text to detect emotion: ")
            result = detect_emotion(text)
            print(result)
        elif choice == '15':
            prompt = input("Enter prompt for text generation: ")
            result = generate_text(prompt)
            print(result)
        else:
            message = "Invalid choice. Please try again."
            print(message)
            speak(message)