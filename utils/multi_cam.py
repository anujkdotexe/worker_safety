import cv2
import threading
import time
import utils.shared as shared

class CameraThread(threading.Thread):
    def __init__(self, source, cam_id, detector, alarm):
        super().__init__(daemon=True)
        self.source = source
        self.cam_id = cam_id
        self.detector = detector
        self.alarm = alarm
        self.running = True
        self.cap = cv2.VideoCapture(int(source) if source.isdigit() else source)

    def run(self):
        while self.running and not shared.shutdown_requested:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.1)
                continue
            
            # Check for violations (upgraded)
            ppe_violations = self.detector.check_ppe(frame)
            is_fall = self.detector.check_fall(frame)
            
            # Trigger alarms
            for violation, confidence in ppe_violations:
                self.alarm.trigger(violation, self.cam_id, confidence)
            if is_fall:
                self.alarm.trigger("FALL", self.cam_id, 1.0)  # Max confidence
                
            # Display (unchanged)
            cv2.imshow(f"Camera {self.cam_id}", frame)
            if cv2.waitKey(1) == ord('q'):
                shared.shutdown_requested = True

    def stop(self):
        self.running = False
        self.cap.release()