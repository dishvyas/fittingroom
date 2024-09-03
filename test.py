import cv2
import mediapipe as mp
import os

# Initialize MediaPipe pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Load the image from the directory
base_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(base_dir, 'static', 'uploads', 'n.jpg')
image = cv2.imread(image_path)

# Convert the image to RGB (MediaPipe expects RGB)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Process the image to detect poses
results = pose.process(image_rgb)

# Define landmark indices
LEFT_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER
RIGHT_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER
LEFT_HIP = mp_pose.PoseLandmark.LEFT_HIP
RIGHT_HIP = mp_pose.PoseLandmark.RIGHT_HIP
NOSE = mp_pose.PoseLandmark.NOSE

if results.pose_landmarks:
    # Draw landmarks on the image with different colors for specific points
    for i, landmark in enumerate(results.pose_landmarks.landmark):
        if i in [LEFT_SHOULDER, RIGHT_SHOULDER, LEFT_HIP, RIGHT_HIP, NOSE]:
            color = (0, 255, 0)  # Green for selected points
        else:
            color = (255, 0, 0)  # Red for other points
        
        # Draw the landmarks
        cv2.circle(image, 
                   (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])), 
                   5, color, -1)

    # Example: Get left shoulder, right shoulder, nose, and hip landmarks
    LS = results.pose_landmarks.landmark[LEFT_SHOULDER]
    RS = results.pose_landmarks.landmark[RIGHT_SHOULDER]
    LH = results.pose_landmarks.landmark[LEFT_HIP]
    RH = results.pose_landmarks.landmark[RIGHT_HIP]
    
    # Calculate midpoint for neck and hips
    TOP = ((LS.x + RS.x) / 2, (LS.y + RS.y) / 2)
    BOT = ((LH.x + RH.x) / 2, (LH.y + RH.y) / 2)

    # Draw the top and bottom points
    cv2.circle(image, (int(TOP[0] * image.shape[1]), int(TOP[1] * image.shape[0])), 10, (0, 0, 255), -1)
    cv2.circle(image, (int(BOT[0] * image.shape[1]), int(BOT[1] * image.shape[0])), 10, (0, 0, 255), -1)

    print(f"Top (Neck) Point: {TOP}")
    print(f"Bottom (Hip) Point: {BOT}")

# Display the image with landmarks
cv2.imshow('Pose', image)
cv2.waitKey(0)
cv2.destroyAllWindows()