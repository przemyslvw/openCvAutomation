import cv2
import time
import numpy as np
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Adres URL kamery IP
url = "rtsp://username:password@IP_ADDRESS:PORT"

# Załaduj model wykrywania obiektów
net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "MobileNetSSD_deploy.caffemodel")

# Lista klas, które model jest w stanie wykryć
CLASSES = ["background", "person", ...]  # Skrócona lista klas

# Funkcja wysyłania powiadomienia e-mail
def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = "twoj_email@gmail.com"
    msg["To"] = "odbiorca_email@gmail.com"
    
    # Użyj SMTP, aby wysłać wiadomość e-mail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("twoj_email@gmail.com", "twoje_haslo")
        server.sendmail("twoj_email@gmail.com", "odbiorca_email@gmail.com", msg.as_string())

# Połączenie z kamerą IP
cap = cv2.VideoCapture(url)
recording = False  # Czy nagrywanie jest aktywne?
alert_sent = False  # Czy wysłano powiadomienie?
connection_lost_alert = False  # Flaga, czy wysłano alert o utracie połączenia

while True:
    ret, frame = cap.read()
    
    # Sprawdzenie, czy połączenie z kamerą jest aktywne
    if not ret:
        print("Utracono połączenie z kamerą.")
        if not connection_lost_alert:
            send_email_alert("Alert: Utrata połączenia z kamerą", 
                             "Połączenie z kamerą IP zostało przerwane.")
            connection_lost_alert = True  # Ustawiamy flagę, żeby wysłać alert tylko raz

        # Próba ponownego połączenia co 5 sekund
        time.sleep(5)
        cap.release()
        cap = cv2.VideoCapture(url)
        continue  # Wracamy do początku pętli, by sprawdzić połączenie po wznowieniu

    # Jeśli połączenie zostało wznowione
    if connection_lost_alert and ret:
        print("Połączenie z kamerą wznowione.")
        send_email_alert("Alert: Połączenie z kamerą wznowione", 
                         "Połączenie z kamerą IP zostało przywrócone.")
        connection_lost_alert = False  # Reset flagi po przywróceniu połączenia

    # Przetwarzanie obrazu, jeśli kamera jest aktywna
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    
    # Przechodzenie przez wykrycia
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        # Jeśli wykryto osobę
        if confidence > 0.5:
            idx = int(detections[0, 0, i, 1])
            if CLASSES[idx] == "person":
                (h, w) = frame.shape[:2]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                
                if not recording:
                    print("Rozpoczynam nagrywanie.")
                    out = cv2.VideoWriter(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi",
                                          cv2.VideoWriter_fourcc(*"XVID"), 20.0, (int(cap.get(3)), int(cap.get(4))))
                    recording = True
                    alert_sent = False  # Resetowanie alertu

                if not alert_sent:
                    send_email_alert("Alert: Wykryto osobę", "Osoba została wykryta w kadrze.")
                    alert_sent = True  # Wysłanie alertu
                    
                out.write(frame)  # Nagrywanie klatki
                
    # Zakończenie nagrywania, gdy brak osób
    if recording and not any([CLASSES[int(detections[0, 0, i, 1])] == "person" for i in range(detections.shape[2])]):
        print("Zakończono nagrywanie.")
        recording = False
        out.release()
        
    cv2.imshow("Kamera IP - Monitoring", frame)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()