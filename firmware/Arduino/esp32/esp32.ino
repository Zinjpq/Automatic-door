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
  #include <HTTPClient.h>

  WebServer server(80);
  HardwareSerial mySerial(1);

  void setup() {
    Serial.begin(115200);
    setup_access_point();
    WiFi.softAP("ESP32-Access Point", "12345678");
    server.begin();
    UnoSerial.begin(9600, SERIAL_8N1, 16, 17);

  }

  void loop() {
    server.handleClient(); // Handle incoming client requests



    //Khi nhan duoc tin hieu tu uno 
    if (UnoSerial.available()) {
      String received = UnoSerial.readStringUntil('\n');
      sendDoorStatus(received);
      // doan nay them cua dang dong hoac da dong 
    }
  }

  void sendDoorStatus(String status) {
    HTTPClient http;
    http.begin("http://192.168.4.184:5000/door_status");
    http.addHeader("Content-Type", "application/json");
    String json = "{\"status\":\"" + status + "\"}";
    int httpResponseCode = http.POST(json);
    http.end();
  }
}
#endif
