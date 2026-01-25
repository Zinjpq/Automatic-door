#include "esp32_cam.h"

String ssid = "Zinj";
String password = "A12345678!";

unsigned long previousMillis = 0;
unsigned long currentMillis = 0;
const long interal = 5000;

IPAddress local_IP(192, 168, 59, 184);
IPAddress gateway(192, 168, 59, 1);
IPAddress subnet(255, 255, 255, 0);

void serveJpg()
{
  auto frame = esp32cam::capture();
  if (frame == nullptr)
  {
    server.send(503, "", "");
    return;
  }
  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}

void handleImage()
{
  if (!esp32cam::Camera.changeResolution(hiRes))
  {
    // camera fail
    for (int i = 0; i < 5; i++)
    {
     debugBlinkLed(2); 
    }
  }
  serveJpg();
}

void setup_cam()
{
  using namespace esp32cam;
  Config cfg;
  cfg.setPins(pins::AiThinker);
  cfg.setResolution(hiRes);
  cfg.setBufferCount(2);
  cfg.setJpeg(80);
  bool ok = Camera.begin(cfg);
}
void ConnectWifi()
{
  WiFi.config(local_IP, gateway, subnet);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED)
  {
    debugBlinkLed(1);
  }
}

void ReconnectWifi()
{
  while (WiFi.status() != WL_CONNECTED)
  {
    debugBlinkLed(1);
  }
  if (currentMillis - previousMillis >= interal)
  {
    if (WiFi.status() != WL_CONNECTED)
    {
      WiFi.disconnect();
      WiFi.begin(ssid, password);
    }
  }
}

void debugBlinkLed(int number)
{
  for (int i = 0; i < number; i++)
  {
    digitalWrite(LED_Debug, LOW);
    delay(250);
    digitalWrite(LED_Debug, HIGH);
    delay(250);
  }
  delay(500);
}
