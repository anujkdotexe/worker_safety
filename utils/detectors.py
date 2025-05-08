from ultralytics import YOLO
import numpy as np

class SafetyDetector:
    def __init__(self):
        self.ppe_model = YOLO("models/yolov8n_ppe.pt")
        self.pose_model = YOLO("models/yolov8_pose.pt")
        
        # Optimize models
        for model in [self.ppe_model, self.pose_model]:
            model.fuse()
            model.overrides['imgsz'] = 320
            model.overrides['conf'] = 0.6

    def check_ppe(self, frame):
        results = self.ppe_model(frame, verbose=False)
        return any(0 in r.boxes.cls.cpu().numpy() for r in results if r.boxes)

    def check_fall(self, frame):
        results = self.pose_model(frame, verbose=False)
        for person in results:
            if person.keypoints is None:
                continue
                
            kpts = person.keypoints.xy.cpu().numpy()[0]
            if len(kpts) >= 13:  # Need nose + hips
                nose, left_hip, right_hip = kpts[0], kpts[11], kpts[12]
                
                # Calculate angles for better fall detection
                vertical = nose[1] - (left_hip[1] + right_hip[1])/2
                horizontal = abs(left_hip[0] - right_hip[0])
                
                # Improved logic
                if abs(vertical) < horizontal * 0.7:  # More sensitive
                    return True
        return False