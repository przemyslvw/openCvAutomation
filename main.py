import cv2

cap = cv2.VideoCapture("http://192.168.0.103:5555/video")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    # Tutaj możesz analizować klatki obrazu
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()