gimport cv2
from utils.detectors import SafetyDetector
from utils.alarms import Alarm
from tkinter import Tk  

def main():
    detector = SafetyDetector()
    alarm = Alarm()
    
    # Read camera sources
    with open("configs/cameras.txt") as f:
        cameras = [line.strip() for line in f.readlines()]
    
    for cam_id, source in enumerate(cameras):
        cap = cv2.VideoCapture(source if not source.isdigit() else int(source))
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            # Detect safety issues
            ppe_violations = detector.check_ppe(frame)
            fall_status = detector.check_fall(frame)
            
            # Trigger alerts
            if ppe_violations:
                print(f"Camera {cam_id}: PPE violation!")
                alarm.trigger()
            if fall_status:
                print(f"Camera {cam_id}: {fall_status}")
                alarm.trigger()
            
            # Display
            cv2.imshow(f"Camera {cam_id}", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()