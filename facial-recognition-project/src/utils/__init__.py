import cv2
import numpy as np

def resize_image(image, width, height):
    """
    Resize the image to the specified width and height.
    """
    return cv2.resize(image, (width, height))

def normalize_image(image):
    """
    Normalize the image to have pixel values between 0 and 1.
    """
    return image / 255.0

def align_face(image, landmarks):
    """
    Align the face in the image based on the provided landmarks.
    """
    # Example implementation using eye landmarks
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    
    # Calculate the angle between the eyes
    dY = right_eye[1] - left_eye[1]
    dX = right_eye[0] - left_eye[0]
    angle = np.degrees(np.arctan2(dY, dX)) - 180
    
    # Calculate the center of the eyes
    eyes_center = ((left_eye[0] + right_eye[0]) // 2, (left_eye[1] + right_eye[1]) // 2)
    
    # Get the rotation matrix
    M = cv2.getRotationMatrix2D(eyes_center, angle, 1)
    
    # Apply the affine transformation
    (h, w) = image.shape[:2]
    aligned_image = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)
    
    return aligned_image

def apply_privacy_mask(image, face_regions):
    """
    Apply a privacy mask to the specified face regions in the image.
    """
    masked_image = image.copy()
    for (x, y, w, h) in face_regions:
        cv2.rectangle(masked_image, (x, y), (x+w, y+h), (0, 0, 0), -1)
    return masked_image