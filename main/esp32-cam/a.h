// source: https://how2electronics.com/esp32-cam-based-object-detection-identification-with-opencv/

#include <WiFi.h>       // Thêm thư viện WiFi
#include <esp32cam.h>   // Thêm thư viện ESP32-CAM
#include <WebServer.h>  // Thêm thư viện WebServer

// Thông tin kết nối WiFi
const char* WIFI_SSID = "Zinj";
const char* WIFI_PASS = "A12345678!";

// Tạo đối tượng web server trên cổng 80
WebServer server(80);

// Định nghĩa cài đặt độ phân giải cao nhất cho camera
static auto hiRes = esp32cam::Resolution::find(800, 600);

// Hàm phục vụ MJPEG stream
void handleMjpegStream(){
  WiFiClient client = server.client();

  const char* header = "HTTP/1.1 200 OK\r\n"
                       "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n\r\n";
  client.print(header);

  while (client.connected()) {
    auto frame = esp32cam::capture();
    if (frame == nullptr) {
      Serial.println("CAPTURE FAIL");
      continue;
    }

    client.printf("--frame\r\nContent-Type: image/jpeg\r\nContent-Length: %d\r\n\r\n", frame->size());
    frame->writeTo(client);
    client.print("\r\n");

    delay(50);  // Điều chỉnh tốc độ khung hình
  }
}

void setupserver(){
  WiFi.softAP(WIFI_SSID, WIFI_PASS);
  IPAddress local_ip(192, 168, 49, 15);
  IPAddress gateway(192, 168, 49, 1);
  IPAddress subnet(255, 255, 255, 0);
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
    cfg.setResolution(hiRes);  // Thiết lập độ phân giải là cao nhất
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
  Serial.println("  /stream");

  // Định nghĩa route cho MJPEG stream
  server.on("/stream", handleMjpegStream);

  server.begin();  // Bắt đầu web server
}

void loop(){
  server.handleClient();  // Xử lý các yêu cầu từ client
}

