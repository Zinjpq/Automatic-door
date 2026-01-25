#ifndef _ESP32_DEV_H__
#define _ESP32_DEV_H__

#include <ESP32Servo.h>
#define SERVOPAN_PIN 18  // trục y dọc
#define SERVOTILT_PIN 19 // trục x ngang

extern String ssid;
extern String password;

WebServer server(80);
HardwareSerial UnoSerial(1);
String doorStatusFromUNO = "UNKNOWN"; // trạng thái nhận từ UNO
Servo panServo, tiltServo;

int pan = 50;
int tilt = 90;











#endif