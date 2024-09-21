#include <WiFi.h>
#include <WebServer.h>

void handleOpenleftdoor(){
  //server.send(200, "text/plain", "Cửa đang mở!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleOpenleftdoor");
  Serial2.print("1");
}

void handleOpen2door(){
  //server.send(200, "text/plain", "Cửa đang mở!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleOpen2door");
  Serial2.print("2");
}

void handleClose(){
  //server.send(200, "text/plain", "Cửa đang đóng!"); // Phản hồi khi nhận yêu cầu 'open'
  Serial.println("handleClose");
  Serial2.print("3");
}

void setup_request(){
  server.on("/openleft", handleOpenleftdoor);
  server.on("/open2", handleOpen2door);
  server.on("/close", handleClose);
}