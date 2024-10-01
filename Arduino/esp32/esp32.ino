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

// Định nghĩa biến toàn cục
// IPAddress local_IP(192, 168, 1, 100);
// IPAddress gateway(192, 168, 1, 1);
// IPAddress subnet(255, 255, 255, 0);

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);

  EEPROM.begin(512); // Khởi tạo EEPROM (kích thước tùy theo nhu cầu)
  if (!EEPROM.begin(512)) {
    Serial.println("EEPROM initialization failed");
    while (true); // Dừng chương trình nếu EEPROM không khởi tạo được
  }

  setup_cam();
  
  // Tải thông tin Wi-Fi từ EEPROM
  String ssid, password;
  loadWiFiCredentials(ssid, password);

  if (ssid != "" && password != "") {
    // WiFi.config(local_IP, gateway, subnet);  // Thiết lập IP tĩnh trước khi kết nối Wi-Fi
    WiFi.begin(ssid.c_str(), password.c_str());
    //WiFi.begin("Zinj", "A12345678!");
    //Serial.print("Đang kết nối tới Wi-Fi");

    int counter = 0;
    while (WiFi.status() != WL_CONNECTED && counter < 20) {
      delay(1000);
      //Serial.print(".");
      counter++;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Đã kết nối tới Wi-Fi");
      Serial.print("Địa chỉ IP: ");
      Serial.println(WiFi.localIP());

      // Thiết lập thời gian, camera và các servo pan-tilt
      //setup_request();
      // setup_pantiltcam();

      // Thiết lập server để xử lý các yêu cầu HTTP
      server.on("/cam", handleImage);
      server.begin();
      return;
    }
    setup_access_point(); // Chuyển sang chế độ AP nếu không có thông tin Wi-Fi
  }
}

void loop() {
  server.handleClient(); // Xử lý các yêu cầu HTTP từ người dùng
}
