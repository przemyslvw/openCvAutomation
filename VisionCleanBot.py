import cv2
import numpy as np

# Inicjalizacja kamerki
cap = cv2.VideoCapture(0)  # 0 oznacza pierwszą podłączoną kamerę

# Parametry robota
robot_position = [50, 50]  # Startowa pozycja robota na wirtualnej mapie (x, y)
robot_direction = [1, 0]  # Robot porusza się w prawo
map_size = (500, 500)     # Rozmiar wirtualnej mapy
obstacle_map = np.zeros(map_size, dtype=np.uint8)  # Wirtualna mapa przeszkód
visited_map = np.zeros(map_size, dtype=np.uint8)   # Wirtualna mapa odwiedzonych obszarów

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
    """Prosty algorytm unikania przeszkód i eksploracji nowych obszarów."""
    global robot_position, robot_direction, visited_map

    # Zaznacz aktualną pozycję jako odwiedzoną
    visited_map[robot_position[1], robot_position[0]] = 255

    # Sprawdź, czy w kierunku ruchu jest przeszkoda lub odwiedzone miejsce
    next_position = [
        robot_position[0] + robot_direction[0] * 10,
        robot_position[1] + robot_direction[1] * 10
    ]
    if (obstacle_map[next_position[1], next_position[0]] == 255 or
        visited_map[next_position[1], next_position[0]] == 255):
        # Zmień kierunek ruchu (rotacja o 90 stopni)
        robot_direction[0], robot_direction[1] = -robot_direction[1], robot_direction[0]

    # Aktualizuj pozycję robota
    robot_position[0] += robot_direction[0] * 10
    robot_position[1] += robot_direction[1] * 10

    # Zabezpieczenie przed wyjściem poza mapę
    robot_position[0] = max(0, min(map_size[0] - 1, robot_position[0]))
    robot_position[1] = max(0, min(map_size[1] - 1, robot_position[1]))

def draw_map():
    """Wyświetlenie wirtualnej mapy z robotem, przeszkodami i odwiedzonymi obszarami."""
    global obstacle_map, visited_map, robot_position

    # Nakładanie przeszkód i odwiedzonych obszarów
    map_display = cv2.cvtColor(visited_map, cv2.COLOR_GRAY2BGR)
    map_display[obstacle_map == 255] = [0, 0, 255]  # Czerwony dla przeszkód
    cv2.circle(map_display, tuple(robot_position), 5, (0, 255, 0), -1)  # Zielony dla robota

    cv2.imshow("Mapa wirtualna", map_display)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie można uzyskać obrazu z kamerki.")
        break

    # Przetwarzanie obrazu
    processed_frame, obstacles = process_frame(frame)

    # Aktualizacja mapy przeszkód
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