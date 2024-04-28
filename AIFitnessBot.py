import cv2
import mediapipe as mp
import numpy as np
from Functions import calculate_angle, determineExercise

mpDrawing = mp.solutions.drawing_utils
mpPose = mp.solutions.pose

exercise = input("1 = Left Bicep Curls, 2 = Right Bicep Curls, 3 = Lateral Raises, 4 = Squats")

a,b,c = determineExercise(exercise)


cap = cv2.VideoCapture(1)

#Curl counter variables
count = 0
stage = None

#setup mediapipe instance

with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:## set accuracy
    while cap.isOpened():
        ret, frame = cap.read()

        #Detections

        #Recoloring Image to RGB
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img.flags.writeable = False

        #Make detection
        result = pose.process(img)

        #Recolor back to BGR
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)


        #Extract Landmarks
        try:
            landmarks = result.pose_landmarks.landmark
            #get coordinates
            shoulder = [landmarks[a].x, landmarks[a].y]
            elbow = [landmarks[b].x,landmarks[b].y]
            wrist = [landmarks[c].x, landmarks[c].y]

            #calc angle
            angle = calculate_angle(shoulder, elbow, wrist)
            cv2.putText(img, str(angle),
                        tuple(np.multiply(elbow, [640, 480]).astype(int)),
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

            #Measure Angle based on user feedback
            if exercise == "1" or exercise == "2":
                if angle > 160:
                    stage = "down"
                if angle <60 and stage =="down":
                    stage = "up"
                    count+=1
                    print(count)
            elif exercise == "3":
                if angle > 145:
                    stage = "down"
                if angle <85 and stage == "down":
                    stage= "up"
                    count+=1
                    print(count)

            elif exercise == "4":
                if angle < 80:
                    stage = "down"
                if angle >160 and stage == "down":
                    stage = "up"
                    count+=1
                    print(count)


        except:
             pass

        #Render counter on screen
        cv2.rectangle(img,(0,0), (300,65), (244,83,28), -1)

        cv2.putText(img, 'REPS', (15,12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(img, str(count),
                    (10,60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)

        cv2.putText(img, 'STAGE', (100, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(img, str(stage),
                    (100, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)


        #Render detections
        mpDrawing.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS,
                                 mpDrawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                 mpDrawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
                                 )


        cv2.imshow('Roneets feed', img)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()



