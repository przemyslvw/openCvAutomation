import cv2
import socket
import struct
import pickle

# Ustawienia socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8485))
server_socket.listen(1)
conn, addr = server_socket.accept()

# Adres URL streamu RTSP
stream_url = "rtsp://192.168.0.101:8080/h264_ulaw.sdp"
cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Tutaj dodaj swoją logikę analizy obrazu za pomocą OpenCV

    # Serializacja danych
    data = pickle.dumps(frame)
    size = len(data)
    
    # Wysyłanie danych z Raspberry Pi do komputera z Windows
    conn.sendall(struct.pack(">L", size) + data)

cap.release()
conn.close()
server_socket.close()
