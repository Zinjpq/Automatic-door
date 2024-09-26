#include <esp32cam.h>

// Sử dụng độ phân giải cao nhất
static auto hiRes = esp32cam::Resolution::find(800, 600);

void serveJpg(){
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    //Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  //Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),static_cast<int>(frame->size()));
  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}

void handleImage(){
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("CAMERA FAIL");
  }
  serveJpg();
}

void setup_cam(){
  Serial.println();
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes); // Đặt độ phân giải cao nhất
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
}