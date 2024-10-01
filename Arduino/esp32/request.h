#include <WiFi.h>
#include <WebServer.h>

void handleOpenleftdoor(){
  // Serial.println("handleOpenleftdoor");
  Serial2.print("1");
}

void handleOpen2door(){
  // Serial.println("handleOpen2door");
  Serial2.print("2");
}

void handleClose(){
  // Serial.println("handleClose");
  Serial2.print("3");
}

void setup_request(){
  server.on("/openleft", handleOpenleftdoor);
  server.on("/open2", handleOpen2door);
  server.on("/close", handleClose);
}