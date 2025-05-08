import time

class Alarm:
    def __init__(self):
        self.last_alert = 0
        
    def trigger(self):
        if time.time() - self.last_alert > 5:  # Throttle alerts
            print("🔔 ALERT: Safety violation detected!")
            self.last_alert = time.time()