import cv2

cap = cv2.VideoCapture(0)  # Change to 1 if webcam not detected
if not cap.isOpened():
    print("❌ Error: Could not open camera")
else:
    print("✅ Camera opened successfully")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Frame read failed")
            break
        cv2.imshow("Test", frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()