#include "esp_camera.h"
#include <WiFi.h>



// WiFi bilgileri
const char *ssid = "H";
const char *password = "11111111";

// Sabit IP yapılandırması
IPAddress local_IP(192, 168, 82, 25);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress primaryDNS(8, 8, 8, 8);
IPAddress secondaryDNS(8, 8, 4, 4);

#define CAMERA_MODEL_AI_THINKER
#include "camera_pins.h"

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println("Booting...");

  // Kamera yapılandırması
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
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 24000000; // Daha hızlı veri işleme için 24 MHz
  config.frame_size = FRAMESIZE_HVGA; // 320x240, FPS için optimize
  config.pixel_format = PIXFORMAT_JPEG;
  config.grab_mode = CAMERA_GRAB_LATEST;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 7; // Düşük kalite, yüksek FPS
  config.fb_count = 1; // Tek çerçeve tamponu

  // PSRAM kontrolü
  if (psramFound()) {
    Serial.println("PSRAM found, using PSRAM for frame buffer");
    config.fb_location = CAMERA_FB_IN_PSRAM;
  } else {
    Serial.println("PSRAM not found, using DRAM");
    config.fb_location = CAMERA_FB_IN_DRAM;
    config.frame_size = FRAMESIZE_QQVGA; // 160x120, daha düşük çözünürlük
  }

  // Kamera başlatma
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    delay(1000);
    ESP.restart();
    return;
  }

  // Sensör ayarları
  sensor_t *s = esp_camera_sensor_get();
  s->set_vflip(s, 1); // Dikey çevirme
  s->set_hmirror(s, 1); // Yatay aynalama (mirror)
  s->set_brightness(s, 0); // Parlaklık (değer: -2 to 2)
  s->set_contrast(s, 0); // Kontrast (değer: -2 to 2)
  s->set_saturation(s, 0); // Doygunluk (değer: -2 to 2)
  s->set_sharpness(s, 0); // Keskinlik (değer: -2 to 2)
  s->set_whitebal(s, 1); // Otomatik beyaz dengesi
  s->set_awb_gain(s, 1); // Otomatik beyaz dengesi kazancı
  s->set_exposure_ctrl(s, 1); // Otomatik pozlama
  s->set_aec_value(s, 300); // Pozlama değeri (0-1200)
  s->set_gain_ctrl(s, 1); // Otomatik kazanç kontrolü

  // Sabit IP ile WiFi bağlantısı
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }

  WiFi.begin(ssid, password);
  WiFi.setSleep(false);

  Serial.print("WiFi connecting");
  int retry_count = 0;
  while (WiFi.status() != WL_CONNECTED && retry_count < 20) {
    delay(1000);
    Serial.print(".");
    retry_count++;
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("\nWiFi connection failed!");
    ESP.restart();
    return;
  }
  Serial.println("\nWiFi connected");

  // Web sunucusunu başlat
  startCameraServer();

  Serial.print("Camera Ready! Use 'http://");
  Serial.print(WiFi.localIP());
  Serial.println("' to connect");
  Serial.println("Stream available at: 'http://" + WiFi.localIP().toString() + "/stream'");
}

void loop() {
  delay(10000); // Gereksiz döngü, kaynak tüketimini azaltır
}