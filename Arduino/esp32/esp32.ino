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
IPAddress local_IP(192, 168, 1, 100);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

int panAngle = 90; // Khai báo biến toàn cục panAngle
int tiltAngle = 90; // Khai báo biến toàn cục tiltAngle

void setup() {
  Serial.begin(115200);
  Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);
  
  WiFi.mode(WIFI_STA);
  WiFi.config(local_IP, gateway, subnet);
  Serial.println("Configuring WiFi with static IP...");

  setup_cam();

  // Tải thông tin Wi-Fi từ EEPROM
  String ssid, password;
  loadWiFiCredentials(ssid, password);

  if (ssid != "" && password != "") {
    WiFi.begin(ssid.c_str(), password.c_str());
    Serial.print("Connecting to Wi-Fi");

    int counter = 0;
    while (WiFi.status() != WL_CONNECTED && counter < 20) {
      delay(1000);
      Serial.print(".");
      counter++;
    }

    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Connected to Wi-Fi");
      Serial.print("IP Address: ");
      Serial.println(WiFi.localIP());

      // Setup time
      setup_request();
      setup_pantiltcam();

      server.on("/cam", handleImage);
      server.begin();
      
      return;
    } else {
      Serial.println("Failed to connect to Wi-Fi");
    }
  }
  setup_access_point(); // Chuyển sang AP nếu không kết nối được Wi-Fi
}

void loop() {
  server.handleClient(); // Duyệt các yêu cầu HTTP từ người dùng
}
