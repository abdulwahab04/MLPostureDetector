# Description: This is the main file for the project. It will be used to run the project.

# Importing the libraries/dependencies
import cv2
import mediapipe as mp 
from utilFunctions import getAngle, warning

# Setting up the mediapipe pose model
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

badFrames = 0

# Setting up the webcam
cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Frame data
        fps = cap.get(cv2.CAP_PROP_FPS)
        h, w = frame.shape[:2]
    
        # Recoloring the frame
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = pose.process(image) # Pose detection
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) # Drawing/rendering detections
        
        # Getting the landmarks and coordinates
        lm = results.pose_landmarks
        lmPose  = mp_pose.PoseLandmark
        
        if not lm:
            continue
        
        # Left shoulder.
        leftShoulderX = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
        leftShoulderY = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)
        
        # Right shoulder.
        rightShoulderX = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
        rightShoulderY = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)
        
        # Left ear.
        leftEarX = int(lm.landmark[lmPose.LEFT_EAR].x * w)
        leftEarY = int(lm.landmark[lmPose.LEFT_EAR].y * h)
        
        # Left hip.
        leftHipX = int(lm.landmark[lmPose.LEFT_HIP].x * w)
        leftHipY = int(lm.landmark[lmPose.LEFT_HIP].y * h)
    
        # Calculating the angles
        neck_angle = getAngle(leftShoulderX, leftShoulderY, rightShoulderX, rightShoulderY)
        torso_angle = getAngle(leftHipX, leftHipY, leftShoulderX, leftShoulderY)
        
        # print(neck_angle, torso_angle)
        
        # Conditions for good and bad posture
        if neck_angle > 60 and torso_angle < 5:
            cv2.putText(image, "Good posture", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            badFrames = 0
        else:
            cv2.putText(image, "Bad posture", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            badFrames += 1
        
        # Calculating the time spent in bad posture
        badPostureTime = badFrames*(1/fps)
        warning(badPostureTime)
        
        cv2.imshow('Feed', image)
        if cv2.waitKey(5) & 0xFF == ord('x'):
            break
    cap.release()
    cv2.destroyAllWindows()