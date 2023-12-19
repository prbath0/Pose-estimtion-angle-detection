import os
import cv2
import time
import math
import mediapipe as mp

class PoseEstimation:
    def __init__(self, video_path):
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()
        self.cap = cv2.VideoCapture(video_path if video_path else 0)
        self.pTime = 0

    def rescale_frame(self, frame, scale):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        dimensions = (width, height)
        return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    def calculate_angle(self, a, b, c):
        radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
        angle = math.degrees(abs(radians))
        return angle

    def process_video(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break

            frame_resized = self.rescale_frame(img, scale=1.4)
            imgRGB = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            results_pose = self.pose.process(imgRGB)

            if results_pose.pose_landmarks:
                self.mpDraw.draw_landmarks(frame_resized, results_pose.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

                # Extract landmarks for right wrist, elbow, and shoulder
                landmarks = results_pose.pose_landmarks.landmark
                rwrist = [landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].y * frame_resized.shape[0]]
                relbow = [landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].y * frame_resized.shape[0]]
                rshoulder = [landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_resized.shape[1],
                            landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_resized.shape[0]]

                # Calculate angle between right wrist, elbow, and shoulder
                angleR = self.calculate_angle(rshoulder, relbow, rwrist)

                # Draw an arc between right elbow and shoulder
                cv2.ellipse(frame_resized, (int(relbow[0]), int(relbow[1])), (50, 50), 0, 0, int(angleR), (255, 255, 0), 2)

                cv2.putText(frame_resized, f'Right angle = {int(angleR) } degrees', (20, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

                lwrist = [landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].y * frame_resized.shape[0]]
                lelbow = [landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y * frame_resized.shape[0]]
                lshoulder = [landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x * frame_resized.shape[1],
                            landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y * frame_resized.shape[0]]

                # Calculate angle between left wrist, elbow, and shoulder
                angleL = self.calculate_angle(lshoulder, lelbow, lwrist)

                # Draw an arc between left elbow and shoulder
                cv2.ellipse(frame_resized, (int(lelbow[0]), int(lelbow[1])), (50, 50), 0, 0, int(angleL), (255, 255, 0), 2)

                # Display measured angle on view

                # Display measured angle on view
                cv2.putText(frame_resized, f'Left angle = {int(angleL)} degrees', (20, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)


            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(frame_resized, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
            cv2.imshow("Video Resized", frame_resized)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                ispaused = True
                while ispaused:
                    if cv2.waitKey(1) & 0xFF == ord('c'):
                        ispaused = False


        self.cap.release()
        # cv2.destroyAllWindows()
        
    def process_image(self, input_image_path):
        img = cv2.imread(input_image_path)
        if img is None:
            print("Could not read the image.")
            return

        frame_resized = self.rescale_frame(img, scale=0.4)
        imgRGB = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        results_pose = self.pose.process(imgRGB)

        if results_pose.pose_landmarks:
            self.mpDraw.draw_landmarks(frame_resized, results_pose.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

            # Extract landmarks for right wrist, elbow, and shoulder
            landmarks = results_pose.pose_landmarks.landmark
            rwrist = [landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].x * frame_resized.shape[1],
                    landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].y * frame_resized.shape[0]]
            relbow = [landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].x * frame_resized.shape[1],
                    landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].y * frame_resized.shape[0]]
            rshoulder = [landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_resized.shape[0]]

            # Calculate angle between right wrist, elbow, and shoulder
            angleR = self.calculate_angle(rshoulder, relbow, rwrist)
            
            # Draw an arc between right elbow and shoulder
            cv2.ellipse(frame_resized, (int(relbow[0]), int(relbow[1])), (50, 50), 0, 0, int(angleR), (255, 255, 0), 2)
            
            cv2.putText(frame_resized, f'Right angle = {int(angleR)} degrees', (20, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
            
            lwrist = [landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].x * frame_resized.shape[1],
                    landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].y * frame_resized.shape[0]]
            lelbow = [landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x * frame_resized.shape[1],
                    landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y * frame_resized.shape[0]]
            lshoulder = [landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y * frame_resized.shape[0]]

            # Calculate angle between left wrist, elbow, and shoulder
            angleL = self.calculate_angle(lshoulder, lelbow, lwrist)
            
            # Draw an arc between left elbow and shoulder
            cv2.ellipse(frame_resized, (int(lelbow[0]), int(lelbow[1])), (50, 50), 0, 0, int(angleL), (255, 255, 0), 2)
            
            # Display measured angle on view
            
            # Display measured angle on view
            cv2.putText(frame_resized, f'Left angle = {int(angleL)} degrees', (20, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 2500, 0), 1)
        

        # Calculate FPS and display
        cTime = time.time()
        fps = 1 / (cTime - self.pTime)
        self.pTime = cTime
        cv2.putText(frame_resized, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Display the analyzed image
        cv2.imshow("Analyzed Image", frame_resized)
        cv2.waitKey(0)  # Wait for any key to be pressed before closing the window
        cv2.destroyAllWindows()
        
    def process_webcam(self):
    
        while True:
            success, img = self.cap.read()
            if not success:
                break
            frame_resized = self.rescale_frame(img, scale=1.6)
            imgRGB = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            results_pose = self.pose.process(imgRGB)

            if results_pose.pose_landmarks:
                self.mpDraw.draw_landmarks(frame_resized, results_pose.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

                # Extract landmarks for right wrist, elbow, and shoulder
                landmarks = results_pose.pose_landmarks.landmark
                rwrist = [landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.RIGHT_WRIST.value].y * frame_resized.shape[0]]
                relbow = [landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.RIGHT_ELBOW.value].y * frame_resized.shape[0]]
                rshoulder = [landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].x * frame_resized.shape[1],
                            landmarks[self.mpPose.PoseLandmark.RIGHT_SHOULDER.value].y * frame_resized.shape[0]]

                # Calculate angle between right wrist, elbow, and shoulder
                angleR = self.calculate_angle(rshoulder, relbow, rwrist)
                
                # Draw an arc between right elbow and shoulder
                cv2.ellipse(frame_resized, (int(relbow[0]), int(relbow[1])), (50, 50), 0, 0, int(angleR), (255, 255, 0), 2)
                
                cv2.putText(frame_resized, f'Right angle = {int(angleR)} degrees', (20, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
                
                lwrist = [landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.LEFT_WRIST.value].y * frame_resized.shape[0]]
                lelbow = [landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].x * frame_resized.shape[1],
                        landmarks[self.mpPose.PoseLandmark.LEFT_ELBOW.value].y * frame_resized.shape[0]]
                lshoulder = [landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].x * frame_resized.shape[1],
                            landmarks[self.mpPose.PoseLandmark.LEFT_SHOULDER.value].y * frame_resized.shape[0]]

                # Calculate angle between left wrist, elbow, and shoulder
                angleL = self.calculate_angle(lshoulder, lelbow, lwrist)
                
                # Draw an arc between left elbow and shoulder
                cv2.ellipse(frame_resized, (int(lelbow[0]), int(lelbow[1])), (50, 50), 0, 0, int(angleL), (255, 255, 0), 2)
                
                # Display measured angle on view
                
                # Display measured angle on view
                cv2.putText(frame_resized, f'Left angle = {int(angleL)} degrees', (20, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
            
            
            cTime = time.time()
            fps = 1 / (cTime - self.pTime)
            self.pTime = cTime
            cv2.putText(frame_resized, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
            cv2.imshow("Webcam Feed", frame_resized)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()