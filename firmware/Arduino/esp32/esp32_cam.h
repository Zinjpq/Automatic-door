#ifndef _ESP32_CAM_H__
#define _ESP32_CAM_H__

#include <esp32cam.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Arduino.h>

#define LED_Debug 33

extern unsigned long currentMillis,previousMillis;
// extern unsigned long previousMillis;
extern const long interal;
extern String ssid;
extern String password;
extern WebServer server;
extern IPAddress local_IP;
extern IPAddress gateway;
extern IPAddress subnet;

static auto hiRes = esp32cam::Resolution::find(800, 600);

void serveJpg();
void handleImage();
void setup_cam();
void debugBlinkLed(int number);
void ReconnectWifi();
void ConnectWifi();

#endif