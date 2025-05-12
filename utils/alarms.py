import time
from datetime import datetime
try:
    from pymongo import MongoClient
except ImportError:
    print("Warning: pymongo not installed. Using console logging only.")
    class MongoClient:
        def __init__(self, *args, **kwargs): pass

class Alarm:
    def __init__(self):
        self.last_alert = 0
        try:
            self.client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
            self.client.server_info()  # Test connection
            self.db = self.client["safety_monitoring"]
            self.incidents = self.db["incidents"]
            self.use_mongo = True
        except Exception as e:
            print(f"MongoDB connection failed: {e}. Using console logging.")
            self.use_mongo = False

    def trigger(self, violation_type, camera_id, confidence):
        """Log to MongoDB or console with 5-second throttling"""
        if time.time() - self.last_alert > 5:
            log_entry = {
                "timestamp": datetime.now(),
                "camera_id": camera_id,
                "violation_type": violation_type,
                "confidence": confidence
            }
            
            if self.use_mongo:
                self.incidents.insert_one(log_entry)
            else:
                print(f"🚨 {log_entry}")
            
            self.last_alert = time.time()