import cv2
import numpy as np

# Inicjalizacja kamerki
cap = cv2.VideoCapture(0)  # 0 oznacza pierwszą podłączoną kamerę

# Parametry robota
robot_position = [50, 50]  # Startowa pozycja robota na wirtualnej mapie (x, y)
robot_direction = [1, 0]  # Robot porusza się w prawo
map_size = (500, 500)     # Rozmiar wirtualnej mapy
obstacle_map = np.zeros(map_size, dtype=np.uint8)  # Wirtualna mapa przeszkód

def process_frame(frame):
    """Przetwarzanie klatki wideo i wykrywanie przeszkód."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Konwersja na HSV
    lower_color = np.array([0, 0, 0])  # Dolny próg (np. czarne obiekty)
    upper_color = np.array([180, 255, 100])  # Górny próg

    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_obstacles = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # Minimalny rozmiar przeszkody
            x, y, w, h = cv2.boundingRect(contour)
            detected_obstacles.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)  # Rysowanie przeszkód

    return frame, detected_obstacles

def update_map(obstacles):
    """Aktualizacja wirtualnej mapy przeszkód."""
    global obstacle_map
    for x, y, w, h in obstacles:
        obstacle_map[y:y+h, x:x+w] = 255  # Oznaczanie przeszkód na mapie

def move_robot(obstacles):
    """Prosty algorytm unikania przeszkód."""
    global robot_position, robot_direction

    # Sprawdź, czy w kierunku ruchu jest przeszkoda
    for x, y, w, h in obstacles:
        if robot_position[0] + robot_direction[0] * 10 in range(x, x + w) and \
           robot_position[1] + robot_direction[1] * 10 in range(y, y + h):
            # Zmień kierunek ruchu (np. na lewo)
            robot_direction[0], robot_direction[1] = -robot_direction[1], robot_direction[0]
            break

    # Aktualizuj pozycję robota
    robot_position[0] += robot_direction[0] * 10
    robot_position[1] += robot_direction[1] * 10

    # Zabezpieczenie przed wyjściem poza mapę
    robot_position[0] = max(0, min(map_size[0] - 1, robot_position[0]))
    robot_position[1] = max(0, min(map_size[1] - 1, robot_position[1]))

def draw_map():
    """Wyświetlenie wirtualnej mapy z robotem i przeszkodami."""
    global obstacle_map, robot_position
    map_display = cv2.cvtColor(obstacle_map, cv2.COLOR_GRAY2BGR)
    cv2.circle(map_display, tuple(robot_position), 5, (0, 255, 0), -1)  # Robot na mapie
    cv2.imshow("Mapa wirtualna", map_display)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można uzyskać obrazu z kamerki.")
        break

    # Przetwarzanie obrazu
    processed_frame, obstacles = process_frame(frame)

    # Aktualizacja mapy
    update_map(obstacles)

    # Ruch robota
    move_robot(obstacles)

    # Wyświetlanie obrazu z kamerki
    cv2.imshow("Kamera odkurzacza", processed_frame)

    # Wyświetlanie wirtualnej mapy
    draw_map()

    # Wyjście z pętli
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnienie zasobów
cap.release()
cv2.destroyAllWindows()