#include <WiFi.h>
#include <WebServer.h>

void handleOpenleftdoor(){
  //server.send(200, "text/plain", "Cửa đang mở!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleOpenleftdoor");
}

void handleOpen2door(){
  //server.send(200, "text/plain", "Cửa đang mở!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleOpen2door");
}

void handleClose(){
  //server.send(200, "text/plain", "Cửa đang đóng!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleClose");
}

void setup_request(){
  server.on("/openleft", handleOpenleftdoor);
  server.on("/open2", handleOpen2door);
  server.on("/close", handleClose);
}

// void setup() {
//   Serial.begin(115200);
//   WiFi.begin(ssid, password);

//   // Kết nối tới WiFi
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(1000);
//     Serial.println("Đang kết nối tới WiFi...");
//   }
  
//   Serial.println("Đã kết nối WiFi!");

//   // Định nghĩa các endpoint (đường dẫn) trên server
//   server.on("/open", handleOpen); // Khi nhận yêu cầu đến đường dẫn /open, gọi hàm handleOpen
//   server.on("/close", handleClose);

//   server.begin(); // Bắt đầu web server
//   Serial.println("Server đã bắt đầu");
// }

// void loop() {
//   server.handleClient(); // Lắng nghe các yêu cầu HTTP
// }
