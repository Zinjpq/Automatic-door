#include <WiFi.h>
#include <WebServer.h>
#include <EEPROM.h>
#include <esp32cam.h>
#include <ESP32Servo.h>
#include "setup-wifi_access-point.h"
#include "request.h"
#include "pan-tilt_servo.h"
#include "setup-esp32-cam.h"

#define RXp2 16
#define TXp2 17

int panAngle = 90;
int tiltAngle = 90;

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);

  setup_cam();

  // Tải thông tin Wi-Fi từ EEPROM
  String ssid, password;
  loadWiFiCredentials(ssid, password);

  if (ssid != "" && password != "") {
    // Cố gắng kết nối Wi-Fi đã lưu
    WiFi.begin(ssid.c_str(), password.c_str());
    Serial.print("Connecting to Wi-Fi");

    int counter = 0;
    while (WiFi.status() != WL_CONNECTED && counter < 10) {
      delay(1000);
      Serial.print(".");
      counter++;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Connected to Wi-Fi");
      Serial.println(WiFi.localIP());

      // Setup time
      setup_request();
      setup_access_point();
      setup_2servo();

      server.on("/cam",handleImage);
      server.begin();
      
      return;
    }
  }
}

void loop() {
  server.handleClient(); // Duyệt các yêu cầu HTTP từ người dùng
}
