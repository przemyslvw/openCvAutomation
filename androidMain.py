import cv2

# Adres URL streamu RTSP
stream_url = "rtsp://192.168.0.103:8080/h264_ulaw.sdp"

# Otwieranie strumienia wideo
cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Tutaj dodaj swoją logikę analizy obrazu za pomocą OpenCV
    
    # Przykładowe wyświetlenie obrazu w terminalu Raspberry Pi
    # cv2.imshow('Stream', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break
    
    # Możesz przesłać klatkę dalej (patrz kolejny krok)

cap.release()
cv2.destroyAllWindows()
