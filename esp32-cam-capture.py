import cv2
import urllib.request
import numpy as np

url = 'http://adres_ip_esp32/capture'

while True:
    # Pobieranie obrazu
    img_resp = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
    img = cv2.imdecode(img_np, -1)

    # Przetwarzanie obrazu w OpenCV
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Obraz z ESP32-CAM", gray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()