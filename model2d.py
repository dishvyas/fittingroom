import numpy as np
from scipy import ndimage
import cv2
import mediapipe as mp
import os

# Base Directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Resize an image to a certain width and height while maintaining aspect ratio
def resize(img, width, height=None):
    if height is not None:
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    else:
        r = float(width) / img.shape[1]
        dim = (width, int(img.shape[0] * r))
        img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return img

# Combine an image that has a transparency alpha channel
def blend_transparent(face_img, overlay_img):
    overlay_img_rgb = overlay_img[:, :, :3]  # RGB channels
    overlay_mask = overlay_img[:, :, 3:]  # Alpha channel

    background_mask = 255 - overlay_mask

    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img_rgb * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

# Function to perform 2D fitting
def get2dfit(TSHIRTLOC, PERSONPIC):
    """
    Perform the 2D fitting on a provided image.
    
    Args:
        TSHIRTLOC (str): Path to the t-shirt image.
        PERSONPIC (str): Path to the person's image.
    
    Saves the result to 'fitted_result.jpg' in the static/uploads directory.
    """
    # Initialize MediaPipe pose solution
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_drawing = mp.solutions.drawing_utils

    # Load the images from the provided paths
    image = cv2.imread(PERSONPIC)
    tshirt_path = TSHIRTLOC

    # Convert the image to RGB (MediaPipe expects RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect poses
    results = pose.process(image_rgb)

    # Define landmark indices
    LEFT_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER
    RIGHT_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER
    LEFT_HIP = mp_pose.PoseLandmark.LEFT_HIP
    RIGHT_HIP = mp_pose.PoseLandmark.RIGHT_HIP

    if results.pose_landmarks:
        # Get left shoulder, right shoulder, left hip, and right hip landmarks
        LS = results.pose_landmarks.landmark[LEFT_SHOULDER]
        RS = results.pose_landmarks.landmark[RIGHT_SHOULDER]
        LH = results.pose_landmarks.landmark[LEFT_HIP]
        RH = results.pose_landmarks.landmark[RIGHT_HIP]

        # Calculate midpoint for neck (TOP) and hips (BOT)
        TOP = ((LS.x + RS.x) / 2, (LS.y + RS.y) / 2)
        BOT = ((LH.x + RH.x) / 2, (LH.y + RH.y) / 2)

        # Calculate width and height for the t-shirt
        tshirt_width = int(abs(LS.x - RS.x) * image.shape[1] * 1.2)  # Slightly wider than shoulder width
        tshirt_height = int(abs(TOP[1] - BOT[1]) * image.shape[0] * 1.2)  # Adjust based on torso height

        # Load and resize the t-shirt image
        tshirt = cv2.imread(tshirt_path, -1)
        tshirt = resize(tshirt, tshirt_width, tshirt_height)

        # Adjust y_offset to align t-shirt's neckline with subject's neckline
        neck_offset_factor = 0.15  # Adjust this factor to move the t-shirt up or down
        x_offset = int(TOP[0] * image.shape[1] - tshirt_width / 2)
        y_offset = int(TOP[1] * image.shape[0] - neck_offset_factor * tshirt_height)

        # Ensure the overlay is within image bounds
        x_offset = max(0, min(x_offset, image.shape[1] - tshirt_width))
        y_offset = max(0, min(y_offset, image.shape[0] - tshirt_height))

        # Create region of interest for blending
        roi = image[y_offset:y_offset + tshirt_height, x_offset:x_offset + tshirt_width]

        # Blend the t-shirt onto the body
        blended = blend_transparent(roi, tshirt)
        image[y_offset:y_offset + tshirt_height, x_offset:x_offset + tshirt_width] = blended

    # Save the fitted image
    final = os.path.join(base_dir, 'static', 'uploads', 'fitted_result.jpg')
    cv2.imwrite(final, image)  # Save the modified image