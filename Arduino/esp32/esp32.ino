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
  // Serial.println("Connecting to Wi-Fi...");

  // Wait for Wi-Fi connection (can be removed if not needed)
  // while (WiFi.status() != WL_CONNECTED) {
  //   delay(100); // Short delay for connection stabilization
  // }

  // Serial.println("\nConnected to Wi-Fi");
  // Serial.print("IP Address: ");
  // Serial.println(WiFi.localIP());

  // Setup server routes
  server.on("/cam", handleImage);
  server.begin();
}

void loop() {
  server.handleClient(); // Handle HTTP requests
}




/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Code for Esp32



// #include <WiFi.h>
// #include <WebServer.h>
// #include <ESP32Servo.h>

// WebServer server(80); // Web server on port 80

// // Servo objects for pan and tilt
// Servo panServo;
// Servo tiltServo;

// // Initial positions for pan and tilt
// int panAngle = 90; // Pan angle starts at 90 degrees
// int tiltAngle = 0; // Tilt angle starts at 0 degrees

// // Maximum and minimum angles
// const int MIN_ANGLE = 0;
// const int MAX_ANGLE = 180;

// void handleRoot() {
//   server.send(200, "text/html", "<h1>Welcome to ESP32 Access Point</h1>");
// }

// void handleSave() {
//   server.send(200, "text/plain", "Wi-Fi info saved");
// }

// void handleLeft() {
//   panAngle = max(MIN_ANGLE, panAngle - 10);
//   panServo.write(panAngle);
//   server.send(200, "text/plain", "Moved Left");
//   Serial.println("Moved Left");
// }

// void handleRight() {
//   panAngle = min(MAX_ANGLE, panAngle + 10);
//   panServo.write(panAngle);
//   server.send(200, "text/plain", "Moved Right");
//   Serial.println("Moved Right");
// }

// void handleUp() {
//   tiltAngle = min(MAX_ANGLE, tiltAngle + 10);
//   tiltServo.write(tiltAngle);
//   server.send(200, "text/plain", "Moved Up");
//   Serial.println("Moved Up");
// }

// void handleDown() {
//   tiltAngle = max(MIN_ANGLE, tiltAngle - 10);
//   tiltServo.write(tiltAngle);
//   server.send(200, "text/plain", "Moved Down");
//   Serial.println("Moved Down");
// }

// void setup_access_point() {
//   WiFi.softAP("ESP32-Access Point", "12345678");
//   Serial.println("Access Point mode started");
//   Serial.print("IP Address: ");
//   Serial.println(WiFi.softAPIP());

//   // Using GPIOs compatible with PWM (adjust if necessary)
//   panServo.attach(12);   // GPIO 12 for pan
//   tiltServo.attach(13);  // GPIO 13 for tilt

//   // Initialize servos to initial angles
//   panServo.write(panAngle);
//   tiltServo.write(tiltAngle);

//   // Set up routes
//   server.on("/", handleRoot);
//   server.on("/save", HTTP_POST, handleSave);
//   server.on("/left", handleLeft);
//   server.on("/right", handleRight);
//   server.on("/up", handleUp);
//   server.on("/down", handleDown);
//   server.begin();

//   Serial.println("Web server started");
// }

// void setup() {
//   Serial.begin(115200);
//   setup_access_point();
// }

// void loop() {
//   server.handleClient(); // Handle incoming client requests
// }








/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
// Code cũ
// #include <WiFi.h>
// #include <WebServer.h>
// #include <EEPROM.h>
// #include <esp32cam.h>
// #include <ESP32Servo.h>
// #include "setup-wifi_access-point.h"
// #include "request.h"
// #include "pan-tilt_servo.h"
// #include "setup-esp32-cam.h"

// #define RXp2 16
// #define TXp2 17

// // Định nghĩa biến toàn cục
// // IPAddress local_IP(192, 168, 1, 100);
// // IPAddress gateway(192, 168, 1, 1);
// // IPAddress subnet(255, 255, 255, 0);

// void setup() {
//   Serial.begin(115200);
//   Serial2.begin(9600, SERIAL_8N1, RXp2, TXp2);

//   EEPROM.begin(512); // Khởi tạo EEPROM (kích thước tùy theo nhu cầu)

//   setup_cam();
  
//   // Tải thông tin Wi-Fi từ EEPROM
//   String ssid, password;
//   loadWiFiCredentials(ssid, password);

//   if (ssid != "" && password != "") {
//     // WiFi.config(local_IP, gateway, subnet);  // Thiết lập IP tĩnh trước khi kết nối Wi-Fi
//     WiFi.begin(ssid.c_str(), password.c_str());
//     //WiFi.begin("Zinj", "A12345678!");
//     //Serial.print("Đang kết nối tới Wi-Fi");

//     int counter = 0;
//     while (WiFi.status() != WL_CONNECTED && counter < 20) {
//       delay(1000);
//       //Serial.print(".");
//       counter++;
//     }

//     if (WiFi.status() == WL_CONNECTED) {
//       // Serial.println("Đã kết nối tới Wi-Fi");
//       // Serial.print("Địa chỉ IP: ");
//       Serial.println(WiFi.localIP());

//       // Thiết lập thời gian, camera và các servo pan-tilt
//       //setup_request();
//       // setup_pantiltcam();

//       // Thiết lập server để xử lý các yêu cầu HTTP
//       server.on("/cam", handleImage);
//       server.begin();
//       return;
//     }
//     setup_access_point(); // Chuyển sang chế độ AP nếu không có thông tin Wi-Fi
//   }
// }

// void loop() {
//   server.handleClient(); // Xử lý các yêu cầu HTTP từ người dùng
// }
