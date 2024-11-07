#include "esp_camera.h"
#include <WiFi.h>
#include <WebServer.h>

// Konfiguracja kamery
#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

const char* ssid = "Twoja_Nazwa_Sieci";
const char* password = "Twoje_Haslo";

WebServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Połączenie z Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Połączono z Wi-Fi!");

  // Inicjalizacja kamery
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.pin_xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  if (psramFound()) {
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // Inicjalizacja kamery
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Błąd inicjalizacji kamery: 0x%x", err);
    return;
  }

  // Ustawienie serwera HTTP
  server.on("/capture", HTTP_GET, captureHandler);
  server.begin();
  Serial.println("Serwer HTTP rozpoczął działanie.");
}

// Funkcja do przechwycenia obrazu i zwrócenia go klientowi
void captureHandler() {
  camera_fb_t * fb = esp_camera_fb_get();
  if (!fb) {
    server.send(503, "image/jpeg", "");
    return;
  }
  server.send(200, "image/jpeg", (const char *)fb->buf, fb->len);
  esp_camera_fb_return(fb);
}

void loop() {
  server.handleClient();
}