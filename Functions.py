
import mediapipe as mp
import numpy as np


mpPose = mp.solutions.pose

#Method to Calculate angle
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

#Function to measure angle based on which exercise was chosen
def determineExercise(exercise):

    if exercise == "1":
        a = mpPose.PoseLandmark.LEFT_SHOULDER.value
        b = mpPose.PoseLandmark.LEFT_ELBOW.value
        c = mpPose.PoseLandmark.LEFT_WRIST.value
    elif exercise == "2":
        a = mpPose.PoseLandmark.RIGHT_SHOULDER.value
        b = mpPose.PoseLandmark.RIGHT_ELBOW.value
        c = mpPose.PoseLandmark.RIGHT_WRIST.value
    elif exercise == "3":
        a = mpPose.PoseLandmark.RIGHT_SHOULDER.value
        b = mpPose.PoseLandmark.RIGHT_ELBOW.value
        c = mpPose.PoseLandmark.RIGHT_HIP.value
    elif exercise == "4":
        a = mpPose.PoseLandmark.LEFT_HIP.value
        b = mpPose.PoseLandmark.LEFT_KNEE.value
        c = mpPose.PoseLandmark.LEFT_ANKLE.value




    return a,b,c