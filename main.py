import cv2
import time
import sys
from utils.detectors import SafetyDetector
from utils.alarms import Alarm
from utils.multi_cam import CameraThread
import utils.shared as shared

def main():
    print("🚀 Starting Worker Safety Monitor - Press Q to quit")
    
    # Initialize components
    detector = SafetyDetector()
    alarm = Alarm()
    
    # Camera sources
    try:
        with open("configs/cameras.txt") as f:
            cameras = [line.strip() for line in f if line.strip()]
    except:
        cameras = ["0"]  # Default webcam
    
    # Start camera threads
    threads = []
    for cam_id, source in enumerate(cameras):
        print(f"📷 Starting camera {cam_id} (source: {source})")
        thread = CameraThread(source, cam_id, detector, alarm)
        thread.start()
        threads.append(thread)
        time.sleep(0.3)
    
    # Main loop
    try:
        while not shared.shutdown_requested:
            if cv2.waitKey(1) & 0xFF == ord('q'):
                shared.shutdown_requested = True
    except KeyboardInterrupt:
        shared.shutdown_requested = True
    finally:
        print("🛑 Shutting down...")
        for t in threads:
            t.stop()
        cv2.destroyAllWindows()
        print("✅ System stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()