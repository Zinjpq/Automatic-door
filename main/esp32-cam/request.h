#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Zinj";       // Thay bằng tên WiFi của bạn
const char* password = "A12345678!"; // Thay bằng mật khẩu WiFi của bạn

WebServer server(80);  // Khởi tạo web server tại cổng 80

void handleOpen() {
  server.send(200, "text/plain", "Cửa đang mở!"); // Phản hồi khi nhận yêu cầu 'open'
  // Thực hiện hành động mở cửa tại đây (nếu cần thiết)
  Serial.println("Cửa đang mở!");
}

void handleClose() {
  server.send(200, "text/plain", "Cửa đang đóng!"); // Phản hồi khi nhận yêu cầu 'open'
  // Thực hiện hành động mở cửa tại đây (nếu cần thiết)
  Serial.println("Cửa đang đóng!");
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  // Kết nối tới WiFi
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Đang kết nối tới WiFi...");
  }
  
  Serial.println("Đã kết nối WiFi!");

  // Định nghĩa các endpoint (đường dẫn) trên server
  server.on("/open", handleOpen); // Khi nhận yêu cầu đến đường dẫn /open, gọi hàm handleOpen
  server.on("/close", handleClose);

  server.begin(); // Bắt đầu web server
  Serial.println("Server đã bắt đầu");
}

void loop() {
  server.handleClient(); // Lắng nghe các yêu cầu HTTP
}
