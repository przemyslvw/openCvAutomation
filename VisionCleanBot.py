import cv2
import numpy as np
from collections import deque

# Inicjalizacja kamerki
cap = cv2.VideoCapture(0)  # 0 oznacza pierwszą podłączoną kamerę

# Parametry robota
robot_position = [50, 50]  # Startowa pozycja robota na wirtualnej mapie (x, y)
robot_start = [50, 50]     # Pozycja startowa robota
robot_direction = [1, 0]   # Robot porusza się w prawo
map_size = (500, 500)      # Rozmiar wirtualnej mapy
obstacle_map = np.zeros(map_size, dtype=np.uint8)  # Wirtualna mapa przeszkód
visited_map = np.zeros(map_size, dtype=np.uint8)   # Wirtualna mapa odwiedzonych obszarów
dock_station = [20, 20]    # Pozycja stacji dokującej
battery_level = 100        # Poziom baterii (0-100)
low_battery_threshold = 20 # Próg niskiego poziomu baterii
charging = False           # Flaga ładowania

# Flaga zakończenia sprzątania
cleaning_done = False

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
    global robot_position, robot_direction, visited_map, cleaning_done, battery_level

    # Zmniejsz poziom baterii
    battery_level -= 1
    if battery_level <= 0:
        print("Bateria rozładowana! Robot zatrzymany.")
        return

    # Zaznacz aktualną pozycję jako odwiedzoną
    visited_map[robot_position[1], robot_position[0]] = 255

    # Sprawdź, czy wszystkie obszary zostały odwiedzone
    if np.all((visited_map + obstacle_map) > 0):
        cleaning_done = True
        print("Sprzątanie zakończone! Powrót do stacji dokującej.")
        return

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

def find_path_to_dock():
    """Wyznacz trasę powrotu do stacji dokującej za pomocą BFS."""
    global robot_position, dock_station, obstacle_map
    queue = deque([(robot_position[0], robot_position[1], [])])  # (x, y, ścieżka)
    visited = set()

    while queue:
        x, y, path = queue.popleft()
        if (x, y) == tuple(dock_station):
            return path  # Znaleziono trasę

        # Dodaj obecny punkt do odwiedzonych
        visited.add((x, y))

        # Sprawdź sąsiednie punkty
        for dx, dy in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < map_size[0] and 0 <= ny < map_size[1] and
                obstacle_map[ny, nx] == 0 and (nx, ny) not in visited):
                queue.append((nx, ny, path + [(nx, ny)]))

    return None  # Brak trasy (teoretycznie niemożliwe)

def draw_map():
    """Wyświetlenie wirtualnej mapy z robotem, przeszkodami, stacją dokującą i odwiedzonymi obszarami."""
    global obstacle_map, visited_map, robot_position, dock_station

    # Nakładanie przeszkód i odwiedzonych obszarów
    map_display = cv2.cvtColor(visited_map, cv2.COLOR_GRAY2BGR)
    map_display[obstacle_map == 255] = [0, 0, 255]  # Czerwony dla przeszkód
    cv2.circle(map_display, tuple(robot_position), 5, (0, 255, 0), -1)  # Zielony dla robota
    cv2.circle(map_display, tuple(dock_station), 5, (255, 0, 0), -1)    # Niebieski dla stacji dokującej

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

    if charging:
        # Symulacja ładowania
        battery_level += 1
        if battery_level >= 100:
            charging = False
            print("Bateria naładowana! Wznowienie sprzątania.")
    elif battery_level <= low_battery_threshold or cleaning_done:
        # Wyznacz trasę do stacji dokującej
        path_to_dock = find_path_to_dock()
        if path_to_dock:
            for pos in path_to_dock:
                robot_position[0], robot_position[1] = pos
                draw_map()
                cv2.waitKey(100)  # Symulacja ruchu
            print("Robot dotarł do stacji dokującej.")
            charging = True
    else:
        # Ruch robota
        move_robot(obstacles)

    # Wyświetlanie obrazu z kamerki
    cv2.imshow("Kamera odkurzacza", processed_frame)

    # Wyświetlanie wirtualnej mapy
    draw_map()

    # Wyjście z pętli
    if cv2.waitKey(1) & 0xFF