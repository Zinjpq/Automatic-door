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
  ////////////////////////////////////////////////////////////
  #define FLASH_PIN 4

  void setup() {
    // Serial.begin(115200);
    setup_cam(); // Initializes the camera module
    WiFi.config(local_IP, gateway, subnet);
    WiFi.begin("ESP32-Access Point", "12345678");
    ////////////////////////////////////////////////////////////
    pinMode(FLASH_PIN, OUTPUT);        // Set flash pin as output
    digitalWrite(FLASH_PIN, LOW);      // Ensure flash is off initially
    // Wait for WiFi connection with timeout
    unsigned long startAttemptTime = millis();
    const unsigned long wifiTimeout = 5000; // 5 seconds

    while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < wifiTimeout) {
        delay(100);
      }

    if (WiFi.status() != WL_CONNECTED) {
      // Serial.println("WiFi connection failed. Turning on flash.");
      digitalWrite(FLASH_PIN, HIGH); // Turn on flash LED
    }
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
  #include <ESP32Servo.h>
  #define SERVOPAN_PIN 18   // trục y dọc
  #define SERVOTILT_PIN 19  // trục x ngang
  Servo panServo, tiltServo;
  int pan = 50;
  int tilt = 90;

  void setup() {
    // Serial.begin(115200);
    WiFi.softAP("ESP32-Access Point", "12345678");
    ////////////////////////////////////////////////////////////
    panServo.attach(SERVOPAN_PIN);  // ngang
    tiltServo.attach(SERVOTILT_PIN); // doc
    panServo.write(pan);
    tiltServo.write(tilt);
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

        panServo.write(pan);
        tiltServo.write(tilt);
        
        // Gui xuong Uno
        String command ="DOOR:" + String(door);
        ////// PAN:90,TILT:90,DOOR:1 "PAN:" + String(pan) + ",TILT:" + String(tilt) + ",
        UnoSerial.println("o");

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
      String incoming = UnoSerial.readStringUntil('\n');
      incoming.trim();

      if (incoming.startsWith("DOOR_STATE:")) {
        doorStatusFromUNO = incoming.substring(strlen("DOOR_STATE:"));
        // Serial.println("Received from UNO: " + doorStatusFromUNO);
      }
    }
    
    // if(doorStatusFromUNO == "OPEN"){
    //   lcd.clear();
    //   lcd.setCursor(0, 0);
    //   lcd.print("Cửa mở");
    // } else if(doorStatusFromUNO == "CLOSED"){
    //   lcd.clear();
    //   lcd.setCursor(0, 0);
    //   lcd.print("Cửa đóng");
    // }
  }

#endif
