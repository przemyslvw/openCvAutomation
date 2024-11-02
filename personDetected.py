import cv2
import time

# Adres URL kamery IP
url = "rtsp://username:password@IP_ADDRESS:PORT"

# Ładowanie modelu MobileNet SSD do wykrywania obiektów
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "MobileNetSSD_deploy.caffemodel")

# Lista klas, które model jest w stanie wykryć
CLASSES = ["background", "person", "bicycle", "car", "motorcycle", "airplane", "bus", 
           "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", 
           "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", 
           "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", 
           "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", 
           "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket", 
           "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", 
           "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", 
           "donut", "cake", "chair", "couch", "potted plant", "bed", "dining table", 
           "toilet", "TV", "laptop", "mouse", "remote", "keyboard", "cell phone", 
           "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", 
           "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]

# Funkcja do nagrywania 5 sekundowego klipu
def record_video(video_source, duration=5):
    # Pobieranie bieżącego czasu
    end_time = time.time() + duration
    
    # Otwieranie połączenia z kamerą IP
    cap = cv2.VideoCapture(video_source)
    
    # Ustawienia zapisu wideo
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter("detected_person.avi", fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
    
    # Nagrywanie przez określony czas
    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
    
    # Zamykanie strumieni
    out.release()
    cap.release()

# Połączenie z kamerą IP
cap = cv2.VideoCapture(url)

# Flaga wykrycia osoby
person_detected = False

while True:
    # Pobieranie klatki z kamery
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się pobrać klatki.")
        break
    
    # Przetwarzanie klatki dla sieci neuronowej
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    
    # Przechodzenie przez wszystkie wykrycia
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        # Jeśli pewność jest wystarczająco wysoka i wykryty obiekt to "person"
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == "person":
                (h, w) = frame.shape[:2]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                
                # Rysowanie prostokąta wokół osoby
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # Wykrycie osoby i uruchomienie zapisu
                if not person_detected:
                    print("Wykryto osobę, rozpoczynam nagrywanie.")
                    person_detected = True
                    record_video(url, duration=5)
                    
                break  # Wychodzimy z pętli, aby uniknąć wielokrotnego nagrywania

    # Wyświetlanie obrazu z oznaczeniem osoby
    cv2.imshow("Kamera IP - Wykrywanie osoby", frame)
    
    # Przerwanie pętli klawiszem 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()