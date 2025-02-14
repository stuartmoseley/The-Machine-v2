# Facial Recognition Project

## Overview
This project is a comprehensive facial recognition system that includes functionalities for face tracking, face recognition, sentiment analysis, emotion detection, and text generation. The system is designed to be highly secure, with features such as file integrity verification, secure storage, and admin authentication.

## Features
- **Face Tracking**: Track faces in real-time using multiple webcams.
- **Face Recognition**: Recognize known faces and log detected faces.
- **Sentiment Analysis**: Analyze the sentiment of text input using TinyBERT.
- **Emotion Detection**: Detect emotions from text input using TinyBERT.
- **Text Generation**: Generate text based on a given prompt using GPT-Neo 125M.
- **Admin Menu**: Comprehensive admin menu for managing the system, including adding/deleting known faces, viewing logs, and updating admin settings.
- **Secure Storage**: Encrypt and securely store sensitive data.
- **File Integrity Verification**: Verify the integrity of critical files at startup.
- **Scheduled Tasks**: Schedule periodic tasks such as deleting unknown faces and restarting the system.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/stuartmoseley/The-Machine.git
    cd The-Machine/facial-recognition-project
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Setup
1. Run the [secure_storage.py](http://_vscodecontentref_/1) script to set up the secure storage:
    ```sh
    python src/secure_storage.py
    ```

2. Run the `download_models.py` script to download and store the models securely:
    ```sh
    python src/download_models.py
    ```

3. Run the `main.py` script to start the application:
    ```sh
    python src/main.py
    ```

## Usage
1. Follow the on-screen instructions to authenticate as the admin and access the admin menu.

## Admin Menu Options
1. **Add Known Face**: Add a new known face to the database.
2. **Delete Known Face**: Delete a known face from the database.
3. **View Unknown Faces**: View all unknown faces detected by the system.
4. **View Logs**: View the log of detected faces.
5. **Clear Logs**: Clear the log of detected faces.
6. **View Face Data**: View detailed face data.
7. **Delete Unknown Faces**: Delete all unknown faces from the database.
8. **Update Admin Face**: Update the admin face used for authentication.
9. **Change Admin Password**: Change the admin password.
10. **System Status**: View the current status of the system.
11. **Manage Watchlist**: Manage the watchlist (not yet implemented).
12. **Exit**: Exit the admin menu.
13. **Analyze Sentiment**: Analyze the sentiment of a given text.
14. **Detect Emotion**: Detect the emotion from a given text.
15. **Generate Text**: Generate text based on a given prompt.

## Dependencies
- `deepface`: Lightweight face recognition and facial attribute analysis.
- `opencv-python`: Library for real-time computer vision.
- `speechrecognition`: Library for performing speech recognition.
- `pyaudio`: Python bindings for PortAudio, the cross-platform audio I/O library.
- [cryptography](http://_vscodecontentref_/2): Package designed to expose cryptographic primitives and recipes to Python developers.
- `pyttsx3`: Text-to-speech conversion library in Python.
- `schedule`: In-process scheduler for periodic jobs.
- `numpy`: Fundamental package for scientific computing with Python.
- `Pillow`: Fork of the Python Imaging Library (PIL).
- `face_recognition`: Simple face recognition library for Python.
- `tensorflow`: Open-source machine learning library for research and production.
- `matplotlib`: Comprehensive library for creating static, animated, and interactive visualizations in Python.
- `transformers`: Provides thousands of pre-trained models to perform tasks on texts such as classification, information extraction, question answering, summarization, translation, text generation, etc. in 100+ languages.

## Security Features
- **Admin Authentication**: Password and facial authentication for admin access.
- **Secure Storage**: Encrypt and securely store sensitive data.
- **File Integrity Verification**: Verify the integrity of critical files at startup.
- **Self-Destruct**: Securely wipe all sensitive data and files after multiple failed authentication attempts.

## Scheduled Tasks
- **Delete Unknown Faces**: Scheduled to run daily at 00:00 UTC.
- **System Restart**: Scheduled to run daily at 00:05 UTC.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.