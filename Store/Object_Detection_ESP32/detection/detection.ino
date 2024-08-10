// source: https://how2electronics.com/esp32-cam-based-object-detection-identification-with-opencv/

#include <WebServer.h>  // Thêm thư viện WebServer
#include <WiFi.h>       // Thêm thư viện WiFi
#include <esp32cam.h>   // Thêm thư viện ESP32-CAM

// Thông tin kết nối WiFi
const char* WIFI_SSID = "Zinj";
const char* WIFI_PASS = "A12345678!";

IPAddress local_ip(192, 168, 49, 15);
IPAddress gateway(192, 168, 49, 1);
IPAddress subnet(255, 255, 255, 0);

// Tạo đối tượng web server trên cổng 80
WebServer server(80);

// Định nghĩa các cài đặt độ phân giải khác nhau cho camera
static auto loRes = esp32cam::Resolution::find(320, 240);
static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(800, 600);

// Hàm chụp và phục vụ hình ảnh JPEG
void serveJpg(){
  auto frame = esp32cam::capture();
  if (frame == nullptr) {  // Kiểm tra nếu chụp thất bại
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);  // Gửi khung hình đã chụp tới client
}

// Hàm xử lý yêu cầu ảnh độ phân giải thấp
void handleJpgLo(){
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}

// Hàm xử lý yêu cầu ảnh độ phân giải cao
void handleJpgHi(){
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

// Hàm xử lý yêu cầu ảnh độ phân giải trung bình
void handleJpgMid(){
  if (!esp32cam::Camera.changeResolution(midRes)) {
    Serial.println("SET-MID-RES FAIL");
  }
  serveJpg();
}

void setupserver(){
  WiFi.softAP(WIFI_SSID, WIFI_PASS);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  delay(100);

  server.begin();
  Serial.println("Set up Server completed!");
}
void setup(){
  Serial.begin(115200);  // Bắt đầu giao tiếp nối tiếp ở tốc độ 115200 baud
  Serial.println();
  {
    using namespace esp32cam;
    Config cfg;  // Tạo đối tượng cấu hình cho camera
    cfg.setPins(pins::AiThinker);  // Thiết lập các chân của camera
    cfg.setResolution(hiRes);  // Thiết lập độ phân giải ban đầu là cao
    cfg.setBufferCount(2);  // Thiết lập số lượng bộ đệm là 2
    cfg.setJpeg(80);  // Thiết lập chất lượng JPEG là 80

    bool ok = Camera.begin(cfg);  // Khởi tạo camera với cấu hình đã chỉ định
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
  
  WiFi.persistent(false);  // Vô hiệu hóa kết nối Wi-Fi liên tục
  WiFi.mode(WIFI_STA);  // Đặt chế độ Wi-Fi là station
  WiFi.begin(WIFI_SSID, WIFI_PASS);  // Kết nối tới mạng Wi-Fi đã chỉ định

  // Chờ kết nối Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("http://");
  Serial.println(WiFi.localIP());  // In địa chỉ IP của thiết bị
  Serial.println("  /cam-lo.jpg");
  Serial.println("  /cam-hi.jpg");
  Serial.println("  /cam-mid.jpg");

  // Định nghĩa các route cho web server
  server.on("/cam-lo.jpg", handleJpgLo);
  server.on("/cam-hi.jpg", handleJpgHi);
  server.on("/cam-mid.jpg", handleJpgMid);

  server.begin();  // Bắt đầu web server
}

void loop(){
  server.handleClient();  // Xử lý các yêu cầu từ client
}

