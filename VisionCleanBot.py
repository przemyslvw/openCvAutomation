import cv2
import numpy as np

# Inicjalizacja kamerki
cap = cv2.VideoCapture(0)  # 0 oznacza pierwszą podłączoną kamerę

# Parametry odkurzacza
robot_position = [0, 0]  # Startowa pozycja robota (x, y)
obstacles = []           # Lista przeszkód

def process_frame(frame):
    """Przetwarzanie klatki wideo i wykrywanie przeszkód."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, threshold = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)

    # Znajdowanie konturów
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Wykrywanie przeszkód
    detected_obstacles = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Minimalny obszar przeszkody
            x, y, w, h = cv2.boundingRect(contour)
            detected_obstacles.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Rysowanie przeszkód

    return frame, detected_obstacles

def move_robot():
    """Prosty algorytm ruchu robota (do rozwoju)."""
    # Przykład: robot porusza się w linii prostej
    robot_position[0] += 1
    print(f"Pozycja robota: {robot_position}")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można uzyskać obrazu z kamerki.")
        break

    # Przetwarzanie obrazu
    processed_frame, obstacles = process_frame(frame)

    # Wyświetlanie obrazu
    cv2.imshow("Kamera odkurzacza", processed_frame)

    # Ruch robota
    move_robot()

    # Wyjście z pętli
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()