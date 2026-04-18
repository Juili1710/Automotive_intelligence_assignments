# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 14:24:11 2026

@author: Lenovo
"""

import cv2
import mediapipe as mp
#import numpy as np

video_path = "driver_video.mp4"  # EDIT THIS

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

cap = cv2.VideoCapture(video_path)

EYE_CLOSED_THRESHOLD = 0.015

def eye_aspect_ratio(landmarks, eye_indices):
    y1 = landmarks[eye_indices[1]].y
    y2 = landmarks[eye_indices[5]].y
    x1 = landmarks[eye_indices[0]].x
    x2 = landmarks[eye_indices[3]].x
    return abs(y2 - y1) / abs(x2 - x1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face in results.multi_face_landmarks:
            landmarks = face.landmark

            left_eye = [33, 159, 158, 133, 153, 144]
            ear = eye_aspect_ratio(landmarks, left_eye)

            if ear < EYE_CLOSED_THRESHOLD:
                state = "Eye Closed"
            else:
                state = "Eye Open"

            cv2.putText(frame, state, (30, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Driver Monitoring", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
