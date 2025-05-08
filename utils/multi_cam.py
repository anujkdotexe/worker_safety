import cv2
import threading
import time
import numpy as np
import utils.shared as shared

class CameraThread(threading.Thread):
    def __init__(self, source, cam_id, detector, alarm):
        super().__init__(daemon=True)
        self.source = source
        self.cam_id = cam_id
        self.detector = detector
        self.alarm = alarm
        self.running = True
        self.last_status = "Initializing..."
        self.last_color = (0, 255, 0)  # Green
        
        # Initialize camera
        self.cap = cv2.VideoCapture(
            int(source) if source.isdigit() else source,
            cv2.CAP_DSHOW
        )
        if not self.cap.isOpened():
            raise RuntimeError(f"Failed to open camera {cam_id}")

        # Camera settings
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def run(self):
        while self.running and not shared.shutdown_requested:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            
            # Process and display frame
            frame = self.process_frame(frame)
            cv2.imshow(f"Camera {self.cam_id}", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                shared.shutdown_requested = True

    def process_frame(self, frame):
        # Run detections every 10 frames
        if int(time.time() * 10) % 10 == 0:
            try:
                ppe_status = self.detector.check_ppe(frame)
                fall_status = self.detector.check_fall(frame)
                
                if ppe_status or fall_status:
                    self.alarm.trigger()
                    self.last_color = (0, 0, 255)  # Red
                    status = []
                    if ppe_status: status.append("PPE VIOLATION")
                    if fall_status: status.append("FALL DETECTED")
                    self.last_status = " | ".join(status)
                else:
                    self.last_color = (0, 255, 0)  # Green
                    self.last_status = "Status: Normal"
            except Exception as e:
                print(f"Detection error: {e}")
        
        # Add status overlay
        cv2.putText(frame, self.last_status, 
                   (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                   0.7, self.last_color, 2)
        return frame

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyWindow(f"Camera {self.cam_id}")