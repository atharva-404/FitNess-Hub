from channels.generic.websocket import WebsocketConsumer
import cv2
import base64
import numpy as np
import threading
import mediapipe as mp

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  
    b = np.array(b)  
    c = np.array(c)  

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360.0 - angle

    return angle

class VideoConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.right_reps = 0
        self.left_reps = 0
        self.camera_on = False
        self.right_arm_up = False  
        self.left_arm_up = False  

    def receive(self, text_data):
        if text_data == "start":
            self.camera_on = True
            self.video_thread = threading.Thread(target=self.stream_video)
            self.video_thread.start()
        elif text_data == "stop":
            self.camera_on = False
        elif text_data == "reset":
            self.right_reps = 0
            self.left_reps = 0
            self.send(text_data=f"reset|0|0")

    def disconnect(self, close_code):
        self.camera_on = False
        if hasattr(self, "capture"):
            self.capture.release()

    def stream_video(self):
        self.capture = cv2.VideoCapture(0)
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        while self.camera_on and self.capture.isOpened():
            ret, frame = self.capture.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 480))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                h, w, _ = frame.shape

                # Right Arm
                right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                               landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

                if right_angle < 40:
                    self.right_arm_up = True
                if right_angle > 150 and self.right_arm_up:
                    self.right_reps += 1
                    self.right_arm_up = False

                # Left Arm
                left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)

                if left_angle < 40:
                    self.left_arm_up = True
                if left_angle > 150 and self.left_arm_up:
                    self.left_reps += 1
                    self.left_arm_up = False

                # Draw Landmarks
                for points in [(right_shoulder, right_elbow, right_wrist),
                               (left_shoulder, left_elbow, left_wrist)]:
                    for i, point in enumerate(points):
                        cx, cy = int(point[0] * w), int(point[1] * h)
                        cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                        if i > 0:
                            prev_cx, prev_cy = int(points[i - 1][0] * w), int(points[i - 1][1] * h)
                            cv2.line(frame, (prev_cx, prev_cy), (cx, cy), (0, 255, 0), 2)

            cv2.putText(frame, f'Right Reps: {self.right_reps}', (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f'Left Reps: {self.left_reps}', (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            self.send(text_data=f"{self.right_reps}|{self.left_reps}|{frame_base64}")
