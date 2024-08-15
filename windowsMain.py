import cv2
import socket
import struct
import pickle

# Ustawienia socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.0.12', 8485))

data = b""
payload_size = struct.calcsize(">L")

while True:
    while len(data) < payload_size:
        packet = client_socket.recv(4096)
        if not packet: break
        data += packet
    
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4096)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    frame = pickle.loads(frame_data)
    
    cv2.imshow('Received Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
