from pymongo import MongoClient
from datetime import datetime
import time

class Alarm:
    def __init__(self):
        self.last_alert = 0
        # Connect to MongoDB
        try:
            self.client = MongoClient("mongodb://localhost:27017/workers_safety", connectTimeoutMS=3000)
            self.db = self.client["worker_safety"]
            self.incidents = self.db["incidents"]
            print("✅ Connected to MongoDB")
        except Exception as e:
            print(f"❌ MongoDB connection failed: {e}")
            self.client = None

    def trigger(self, violation_type, camera_id, confidence):
        if time.time() - self.last_alert > 5:  # Throttle alerts
            log_entry = {
                "timestamp": datetime.now(),
                "camera_id": camera_id,
                "violation": violation_type,
                "confidence": float(confidence)
            }
            
            if self.client:  # Only log if MongoDB is connected
                self.incidents.insert_one(log_entry)
            
            print(f"🚨 ALERT: {violation_type} (Camera: {camera_id}, Confidence: {confidence:.2f})")
            self.last_alert = time.time()