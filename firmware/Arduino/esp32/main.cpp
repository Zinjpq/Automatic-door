// --- AUTOMATIC CONFIGURATION ---
// DOIT ESP32 DEVKIT V1
// AI Thinker ESP32-CAM

#if defined(BOARD_HAS_PSRAM)
#define IS_ESP32_CAM 1
#else
#define IS_ESP32_CAM 0
#endif

#include <WebServer.h>
#include <WiFi.h>

#if IS_ESP32_CAM
#include "esp32_cam.h"

WebServer server(80);

void setup()
{
  pinMode(LED_Debug, OUTPUT);
  digitalWrite(LED_Debug, HIGH);

  ConnectWifi();
  setup_cam();

  server.on("/cam", handleImage);
  server.begin();
}

void loop()
{
  currentMillis = millis();
  ReconnectWifi();
  server.handleClient();
}

#else

#include "esp32dev.h"

void setup()
{
  
}

void loop()
{
  
}

#endif
