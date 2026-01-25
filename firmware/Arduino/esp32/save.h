WiFi.softAP("ESP32-Access Point", "12345678");
panServo.attach(SERVOPAN_PIN);   // ngang
tiltServo.attach(SERVOTILT_PIN); // doc
panServo.write(pan);
tiltServo.write(tilt);
UnoSerial.begin(9600, SERIAL_8N1, 16, 17);
// server set angle + door status
server.on("/set_angle", []()
          {
      if (server.hasArg("pan") && server.hasArg("tilt")) {
        // Khai bao 
        int pan = server.arg("pan").toInt();
        int tilt = server.arg("tilt").toInt();

        panServo.write(pan);
        tiltServo.write(tilt);
        
        // UnoSerial.println("o");

        server.send(200, "text/plain", "OK");
      } else {
        server.send(400, "text/plain", "Missing parameters");
      } });
server.on("/door_state", []()
          {
      if (server.hasArg("state")) {
        int state = server.arg("state").toInt();

        if (state == 0 || state == 1) {
          String command = "DOOR:" + String(state);
          UnoSerial.println('o'); // Gửi lệnh xuống Uno

          server.send(200, "text/plain", "Door state set to " + String(state));
        } else {
          server.send(400, "text/plain", "Invalid state value (must be 0 or 1)");
        }
      } else {
        server.send(400, "text/plain", "Missing state parameter");
      } });
server.on("/door_status", []()
          { server.send(200, "text/plain", "Door status: " + doorStatusFromUNO); });
server.begin();

// loop///////////////

server.handleClient(); // Handle incoming client requests

// Nhận dữ liệu từ UNO R3
if (UnoSerial.available())
{
  String incoming = UnoSerial.readStringUntil('\n');
  incoming.trim();

  if (incoming.startsWith("DOOR_STATE:"))
  {
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