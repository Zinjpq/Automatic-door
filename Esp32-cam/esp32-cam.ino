#include <WiFi.h>
#include <WebServer.h>
#include <EEPROM.h>
#include "access_point.h"
#include "request.h"
#include "2-axis_servo.h"
#include "cam.h"
#include <esp32cam.h>

void setup() {
  Serial.begin(115200);

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

      setup_request();
      setup_access_point();
      
      server.on("/cam",handleImage);
      server.begin();
      
      return;
    }
  }
}

void loop() {
  server.handleClient(); // Duyệt các yêu cầu HTTP từ người dùng
}
