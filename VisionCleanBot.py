import cv2
import numpy as np
from heapq import heappop, heappush

# Inicjalizacja kamerki
cap = cv2.VideoCapture(0)

# Parametry robota
robot_position = [50, 50]
robot_start = [50, 50]
map_size = (500, 500)
obstacle_map = np.zeros(map_size, dtype=np.uint8)
visited_map = np.zeros(map_size, dtype=np.uint8)
dock_station = [20, 20]
battery_level = 100
low_battery_threshold = 20
charging = False

# Flaga zakończenia sprzątania
cleaning_done = False

def process_frame(frame):
    """Przetwarzanie klatki wideo i wykrywanie przeszkód."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_color = np.array([0, 0, 0])
    upper_color = np.array([180, 255, 100])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_obstacles = []
    for contour in contours:
        if cv2.contourArea(contour) > 100:
            x, y, w, h = cv2.boundingRect(contour)
            detected_obstacles.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

    return frame, detected_obstacles

def update_map(obstacles):
    """Aktualizacja mapy przeszkód."""
    global obstacle_map
    for x, y, w, h in obstacles:
        obstacle_map[y:y+h, x:x+w] = 255

def a_star_search(start, goal):
    """Algorytm A* do wyznaczania najkrótszej trasy."""
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in [(-10, 0), (10, 0), (0, -10), (0, 10)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < map_size[0] and 0 <= neighbor[1] < map_size[1]:
                if obstacle_map[neighbor[1], neighbor[0]] == 255:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], neighbor))

    return None

def find_nearest_unvisited():
    """Znajdź najbliższy nieodwiedzony punkt."""
    global visited_map, obstacle_map
    for y in range(0, map_size[1], 10):
        for x in range(0, map_size[0], 10):
            if visited_map[y, x] == 0 and obstacle_map[y, x] == 0:
                return (x, y)
    return None

def move_robot_to(target):
    """Przesuń robota do wyznaczonego celu."""
    global robot_position
    path = a_star_search(tuple(robot_position), target)
    if path:
        for pos in path:
            robot_position[0], robot_position[1] = pos
            draw_map()
            cv2.waitKey(100)
    else:
        print("Nie można znaleźć ścieżki do celu!")

def draw_map():
    """Wyświetlenie mapy z robotem, przeszkodami i odwiedzonymi obszarami."""
    global obstacle_map, visited_map, robot_position, dock_station
    map_display = cv2.cvtColor(visited_map, cv2.COLOR_GRAY2BGR)
    map_display[obstacle_map == 255] = [0, 0, 255]
    cv2.circle(map_display, tuple(robot_position), 5, (0, 255, 0), -1)
    cv2.circle(map_display, tuple(dock_station), 5, (255, 0, 0), -1)
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
        battery_level += 1
        if battery_level >= 100:
            charging = False
            print("Bateria naładowana! Wznowienie sprzątania.")
    elif battery_level <= low_battery_threshold or cleaning_done:
        move_robot_to(tuple(dock_station))
        charging = True
    else:
        nearest_target = find_nearest_unvisited()
        if nearest_target:
            move_robot_to(nearest_target)
            visited_map[robot_position[1], robot_position[0]] = 255
        else:
            cleaning_done = True
            print("Sprzątanie zakończone! Powrót do stacji dokującej.")
            move_robot_to(tuple(dock_station))
            charging = True

    cv2.imshow("Kamera odkurzacza", processed_frame)
    draw_map()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()