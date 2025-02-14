import cv2
import os
from datetime import datetime
from face_recognition import recognize_faces, search_face_by_id, update_face_database
from face_tracking import track_faces
from admin import admin_menu, scan_for_admin_face, authenticate_admin, verify_file_hashes, restore_files_from_backup, self_destruct, clear_logs, view_logs, view_known_faces, delete_known_face, view_unknown_faces, delete_unknown_faces, update_admin_face, change_admin_password, system_status, create_backup, manage_watchlist, analyze_sentiment, detect_emotion
import pyttsx3
import getpass
import schedule
import time
import sys
from transformers import pipeline

FILES_TO_MONITOR = ["admin.py", "main.py", "face_recognition.py", "face_tracking.py", "secure_storage.py"]

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def save_unknown_face(frame, face_region, source):
    x, y, w, h = face_region
    face_img = frame[y:y+h, x:x+w]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"facebase/unknown_faces/{source}_{timestamp}.jpg"
    cv2.imwrite(filename, face_img)
    message = f"Unknown face saved: {filename}"
    print(message)
    speak(message)

def log_detected_face(face_info, source, sentiment=None, emotion=None):
    with open("facebase/detected_faces.log", "a") as log_file:
        log_entry = f"{datetime.now()} - {source} - {face_info}"
        if sentiment:
            log_entry += f" - Sentiment: {sentiment}"
        if emotion:
            log_entry += f" - Emotion: {emotion}"
        log_file.write(log_entry + "\n")

def search_face(face_id):
    cap1 = cv2.VideoCapture(0)  # Built-in webcam
    cap2 = cv2.VideoCapture(1)  # USB webcam

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        # Track faces in both frames
        faces1 = track_faces(frame1, "Built-in Webcam")
        faces2 = track_faces(frame2, "USB Webcam")

        for face in faces1:
            if search_face_by_id(face_id, frame1, face):
                message = f"Face with ID {face_id} found in Built-in Webcam feed."
                print(message)
                speak(message)
                cap1.release()
                cap2.release()
                cv2.destroyAllWindows()
                return

        for face in faces2:
            if search_face_by_id(face_id, frame2, face):
                message = f"Face with ID {face_id} found in USB Webcam feed."
                print(message)
                speak(message)
                cap1.release()
                cap2.release()
                cv2.destroyAllWindows()
                return

        # Display the frames
        cv2.imshow('Built-in Webcam', frame1)
        cv2.imshow('USB Webcam', frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()
    message = f"Face with ID {face_id} not found."
    print(message)
    speak(message)

# Load TinyBERT for sentiment analysis and emotion detection
tinybert = pipeline('sentiment-analysis', model='prajjwal1/bert-tiny', cache_dir='AI')

# Load GPT-Neo 125M for text generation
gpt_neo = pipeline('text-generation', model='EleutherAI/gpt-neo-125M', cache_dir='AI')

def analyze_sentiment(text):
    result = tinybert(text)
    return result

def detect_emotion(text):
    result = tinybert(text)
    return result

def generate_text(prompt):
    result = gpt_neo(prompt, max_length=50)
    return result

def main():
    # Initialize video capture for both webcams
    cap1 = cv2.VideoCapture(0)  # Built-in webcam
    cap2 = cv2.VideoCapture(1)  # USB webcam

    while True:
        ret1, frame1 = cap1.read()
        ret2 = cap2.read()

        if not ret1 or not ret2:
            break

        # Track and recognize faces in both frames
        faces1 = track_faces(frame1, "Built-in Webcam")
        faces2 = track_faces(frame2, "USB Webcam")

        for face in faces1:
            face_info = recognize_faces(frame1, face, "Built-in Webcam")
            if face_info == "Unknown":
                save_unknown_face(frame1, face, "Built-in Webcam")
            log_detected_face(face_info, "Built-in Webcam")

        for face in faces2:
            face_info = recognize_faces(frame2, face, "USB Webcam")
            if face_info == "Unknown":
                save_unknown_face(frame2, face, "USB Webcam")
            log_detected_face(face_info, "USB Webcam")

        # Display the frames
        cv2.imshow('Built-in Webcam', frame1)
        cv2.imshow('USB Webcam', frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap1.release()
    cap2.release()
    cv2.destroyAllWindows()

def shutdown_and_restart():
    # Perform shutdown tasks
    create_backup(FILES_TO_MONITOR)
    message = "System is shutting down for scheduled maintenance."
    print(message)
    speak(message)
    
    # Restart the script
    python = sys.executable
    os.execl(python, python, *sys.argv)

if __name__ == "__main__":
    # Verify file hashes at startup
    verified, file_path = verify_file_hashes(FILES_TO_MONITOR)
    if not verified:
        message = f"File integrity check failed for {file_path}. Reverting to previous version."
        print(message)
        speak(message)
        restore_files_from_backup()
        self_destruct()

    # Schedule the deletion of unknown faces at 00:00 UTC every day
    schedule.every().day.at("00:00").do(delete_unknown_faces)

    # Schedule a full script shutdown and restart at 00:05 UTC every day
    schedule.every().day.at("00:05").do(shutdown_and_restart)

    # Run the scheduled tasks in a separate thread
    while True:
        schedule.run_pending()
        time.sleep(1)

    # Scan for admin face before starting the system
    if scan_for_admin_face():
        if authenticate_admin():
            main()
            while True:
                message = "\nAdmin Menu:\n1. Admin System\n2. Search Face by ID\n3. View Detected Faces Log\n4. Clear Logs\n5. View Known Faces\n6. Delete Known Face\n7. View Unknown Faces\n8. Delete Unknown Faces\n9. Update Admin Face\n10. Change Admin Password\n11. System Status\n12. Manage Watchlist\n13. Exit\n14. Analyze Sentiment\n15. Generate Text\n16. Detect Emotion"
                print(message)
                speak("Say your command")
                choice = input("Enter your choice: ")

                if choice == '1':
                    admin_menu()
                elif choice == '2':
                    face_id = input("Enter the face ID to search: ")
                    search_face(face_id)
                elif choice == '3':
                    view_logs()
                elif choice == '4':
                    clear_logs()
                elif choice == '5':
                    view_known_faces()
                elif choice == '6':
                    face_id = input("Enter the face ID to delete: ")
                    delete_known_face(face_id)
                elif choice == '7':
                    view_unknown_faces()
                elif choice == '8':
                    delete_unknown_faces()
                elif choice == '9':
                    update_admin_face()
                elif choice == '10':
                    change_admin_password()
                elif choice == '11':
                    system_status()
                elif choice == '12':
                    manage_watchlist()
                elif choice == '13':
                    break
                elif choice == '14':
                    text = input("Enter text to analyze sentiment: ")
                    result = analyze_sentiment(text)
                    print(result)
                elif choice == '15':
                    prompt = input("Enter prompt for text generation: ")
                    result = generate_text(prompt)
                    print(result)
                elif choice == '16':
                    text = input("Enter text to detect emotion: ")
                    result = detect_emotion(text)
                    print(result)
                else:
                    message = "Invalid choice. Please try again."
                    print(message)
                    speak(message)
        else:
            message = "Authentication failed. System locked."
            print(message)
            speak(message)
    else:
        message = "Admin face not detected. System locked."
        print(message)
        speak(message)