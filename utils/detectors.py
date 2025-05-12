from ultralytics import YOLO
import numpy as np
from collections import deque

class SafetyDetector:
    def __init__(self):
        self.ppe_model = YOLO("models/yolov8n_ppe.pt")
        self.pose_model = YOLO("models/yolov8_pose.pt")
        self.pose_history = deque(maxlen=10)  # For temporal analysis
        
        # Optimize models
        for model in [self.ppe_model, self.pose_model]:
            model.fuse()
            model.overrides['imgsz'] = 320
            model.overrides['conf'] = 0.6

    def check_ppe(self, frame):
        """Returns list of (violation_type, confidence) tuples"""
        results = self.ppe_model(frame, verbose=False)
        violations = []
        for r in results:
            if r.boxes:
                for cls, conf in zip(r.boxes.cls.cpu().numpy(), r.boxes.conf.cpu().numpy()):
                    if cls == 0:  # Class 0 = no helmet
                        violations.append(("NO_HELMET", float(conf)))
        return violations

    def check_fall(self, frame):
        """Enhanced fall detection using vector math"""
        results = self.pose_model(frame, verbose=False)
        for person in results:
            if person.keypoints is None:
                continue
                
            kpts = person.keypoints.xy.cpu().numpy()[0]
            if len(kpts) < 13:
                continue

            # Keypoints
            nose, left_hip, right_hip = kpts[0], kpts[11], kpts[12]
            mid_hip = (left_hip + right_hip) / 2
            
            # Vector math
            vertical = nose[1] - mid_hip[1]  # Y-axis difference
            horizontal = abs(left_hip[0] - right_hip[0])  # Hip width
            
            # Temporal analysis
            self.pose_history.append(vertical)
            velocity = 0
            if len(self.pose_history) >= 5:
                velocity = np.mean(np.diff(list(self.pose_history)[-5:]))
            
            # Fall conditions
            is_horizontal = abs(vertical) < horizontal * 0.5
            is_fast_fall = velocity > 10
            
            if is_horizontal or is_fast_fall:
                return True
        return False