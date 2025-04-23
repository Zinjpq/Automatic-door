// Chọn loại ESP32
#define ESP_TYPE 2  // 1 = esp32-cam, 2 = esp32

#if ESP_TYPE == 1
  // Code for Esp32-cam
  #include <WiFi.h>
  #include <esp32cam.h>
  #include <WebServer.h>
  #include "setup-esp32-cam.h"

  WebServer server(80); // Defines server as a global variable

  // Configure static IP settings
  IPAddress local_IP(192, 168, 4, 184);       // Set your desired static IP
  IPAddress gateway(192, 168, 4, 1);          // Typically the router's IP
  IPAddress subnet(255, 255, 255, 0);         // Subnet mask

  void setup() {
    Serial.begin(115200);
    
    setup_cam(); // Initializes the camera module
    
    // Attempt to configure a static IP
    if (!WiFi.config(local_IP, gateway, subnet)) {
      Serial.println("Static IP configuration failed.");
    }
    WiFi.begin("ESP32-Access Point", "12345678");
    // Setup server routes
    server.on("/cam", handleImage);
    server.begin();
  }

  void loop() {
    server.handleClient(); // Handle HTTP requests
  }

#elif ESP_TYPE == 2
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  // Code for Esp32
  #include <WiFi.h>
  #include <WebServer.h>
  // #include <HTTPClient.h>
  WebServer server(80);
  ////////////////////////////////////////////////////////////
  HardwareSerial UnoSerial(1);
  ////////////////////////////////////////////////////////////
  String doorStatusFromUNO = "UNKNOWN"; // trạng thái nhận từ UNO
  ////////////////////////////////////////////////////////////
  #include <LiquidCrystal_I2C.h>
  LiquidCrystal_I2C lcd(0x27, 16, 2);  

  void setup() {
    Serial.begin(115200);
    WiFi.softAP("ESP32-Access Point", "12345678");
    ////////////////////////////////////////////////////////////
    // khoi tao lcd i2c
    lcd.init();
    lcd.backlight();
    ////////////////////////////////////////////////////////////
    UnoSerial.begin(9600, SERIAL_8N1, 16, 17);
    ////////////////////////////////////////////////////////////
    // server set angle + door status
    server.on("/set_angle", []() {
      if (server.hasArg("pan") && server.hasArg("tilt")&& server.hasArg("door")) {
        // Khai bao 
        int pan = server.arg("pan").toInt();
        int tilt = server.arg("tilt").toInt();
        int door = server.arg("door").toInt();
        // Gui xuong Uno
        String command = "PAN:" + String(pan) + ",TILT:" + String(tilt) + ",DOOR:" + String(door);
        UnoSerial.println(command);
        // Check lai
        // Serial.println("Received pan: " + String(pan) + ", tilt: " + String(tilt) + ", door: " + String(door));
        
        // test bang lcd
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.println("pan: " + String(pan) + ", tilt: " + String(tilt));
        lcd.setCursor(0, 1);
        lcd.println(", door: " + String(door));

        server.send(200, "text/plain", "OK");
      } else {
        server.send(400, "text/plain", "Missing parameters");
      }
    });
    // server door status
    server.on("/door_status", []() {
      server.send(200, "text/plain", "Door status: " + doorStatusFromUNO);
    });
    server.begin();
  }

  void loop() {
    server.handleClient(); // Handle incoming client requests

    // Nhận dữ liệu từ UNO R3
    if (UnoSerial.available()) {
      String incoming = Serial2.readStringUntil('\n');
      incoming.trim();

      if (incoming.startsWith("DOOR_STATE:")) {
        doorStatusFromUNO = incoming.substring(strlen("DOOR_STATE:"));
        Serial.println("Received from UNO: " + doorStatusFromUNO);
      }
    }
  }

#endif
