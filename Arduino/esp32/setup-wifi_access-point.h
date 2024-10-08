#include <WebServer.h>

WebServer server(80);

// Hàm tải thông tin Wi-Fi từ EEPROM
void loadWiFiCredentials(String &ssid, String &password) {
  EEPROM.begin(512);
  char ssidChars[100];
  char passwordChars[100];

  for (int i = 0; i < 100; ++i) {
    ssidChars[i] = EEPROM.read(i);
    if (ssidChars[i] == '\0') break;
  }
  ssid = String(ssidChars);

  for (int i = 0; i < 100; ++i) {
    passwordChars[i] = EEPROM.read(100 + i);
    if (passwordChars[i] == '\0') break;
  }
  password = String(passwordChars);
}

// Hàm lưu thông tin Wi-Fi vào EEPROM
void saveWiFiCredentials(String ssid, String password) {
  EEPROM.begin(512); // Khởi tạo EEPROM (kích thước tùy theo nhu cầu)
  // Xóa dữ liệu cũ trong EEPROM
  for (int i = 0; i < 100; ++i) {
    EEPROM.write(i, 0);         // Xóa SSID cũ
    EEPROM.write(100 + i, 0);   // Xóa Password cũ
  }

  for (int i = 0; i < ssid.length(); ++i) {
    EEPROM.write(i, ssid[i]); // Lưu SSID vào EEPROM
  }
  EEPROM.write(ssid.length(), '\0'); // Kết thúc chuỗi SSID

  for (int i = 0; i < password.length(); ++i) {
    EEPROM.write(100 + i, password[i]); // Lưu Password từ địa chỉ 100
  }
  EEPROM.write(100 + password.length(), '\0'); // Kết thúc chuỗi Password

  EEPROM.commit(); // Ghi dữ liệu xuống bộ nhớ
}

// Hàm xử lý yêu cầu của người dùng khi truy cập trang chủ
void handleRoot() {
  String html = "<html><body><h1>Wi-Fi Configuration</h1>";
  html += "<form action='/save' method='POST'>";
  html += "SSID: <input type='text' name='ssid'><br>";
  html += "Password: <input type='text' name='password'><br>";
  html += "<input type='submit' value='Save'>";
  html += "</form></body></html>";

  server.send(200, "text/html", html);
}

// Hàm xử lý khi người dùng gửi form để lưu thông tin Wi-Fi
void handleSave() {
  String ssid = server.arg("ssid");
  String password = server.arg("password");

  // Lưu thông tin Wi-Fi vào EEPROM
  saveWiFiCredentials(ssid, password);
  Serial.println("SSID: " + ssid);
  Serial.println("Password: " + password);

  if (ssid == "" || password == "") {
    server.send(400, "text/html", "SSID hoặc mật khẩu không hợp lệ.");
    return;
  }

  // Thông báo cho người dùng
  String message = "<html><body><h1>Wi-Fi Information Saved!</h1><p>ESP32 will now restart.</p></body></html>";
  server.send(200, "text/html", message);

  delay(2000); // Đợi 2 giây trước khi khởi động lại
  ESP.restart(); // Khởi động lại ESP32
}

void setup_access_point(){
  // Nếu không kết nối được, chuyển sang AP mode
  WiFi.softAP("ESP32-Access Point", "12345678");
  // Serial.println("Failed to connect. Access Point mode started");
  // Serial.println(WiFi.softAPIP());
  WiFi.softAPIP();
  analogWrite(4, (255*1/100));

  // Khởi động web server
  server.on("/", handleRoot); // Trang chủ
  server.on("/save", HTTP_POST, handleSave); // Xử lý lưu thông tin Wi-Fi
  server.begin();
}