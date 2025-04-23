// Cau hinh cho RFID
#include <SPI.h>
#include <MFRC522.h>
#define SS_PIN 10 
#define RST_PIN 9  
// RST   9
// SDA   10
// MOSI  11
// MISO  12
// SCK   13
MFRC522 rfid(SS_PIN, RST_PIN);
// Init array that will store new NUID 
byte nuidPICC[4];
////////////////////////////////////////////////////////////
// Cau hinh servo
#include "Servo.h"
#define SERVOPAN_PIN 5
#define SERVOTILT_PIN 6
#define SERVO360_PIN 3
Servo panservo, tiltservo, servo360;
int pan = 90;
int tilt = 50;
int time = 12;
////////////////////////////////////////////////////////////
// Cau hinh cam bien hong ngoai
#define infraredsensor 1
// Cam bien hanh trinh
#define positionsensor0 A0  // Cam bien khi dong 
#define positionsensor1 A1  // Cam bien khi mo
////////////////////////////////////////////////////////////
// Cau hinh cho UART 
#include <Arduino.h>
String uartBuffer = "";
////////////////////////////////////////////////////////////
// Cau hinh cho FreeRTOS
#include <Arduino_FreeRTOS.h>
#include <task.h>
// Biến dùng để truyền lệnh vào task
String receivedCommand = "";
bool newCommandAvailable = false;


void setup() {
  Serial.begin(9600);
  ////////////////////////////////////////////////////////////
  // RFID
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  ////////////////////////////////////////////////////////////
  // Setup servo
  panservo.attach(SERVOPAN_PIN);  // ngang
  tiltservo.attach(SERVOTILT_PIN); // doc
  servo360.attach(SERVO360_PIN);
  panservo.write(pan);
  tiltservo.write(tilt);
  servo360.write(90);
  ////////////////////////////////////////////////////////////
  // Cau hinh chan cam bien
  pinMode(infraredsensor, INPUT);
  pinMode(positionsensor0,INPUT);
  pinMode(positionsensor1, INPUT);
  ////////////////////////////////////////////////////////////
  // Cau hinh LCD
  // lcd.init();
  ////////////////////////////////////////////////////////////
  while (!Serial) 
  {
    ; // wait for serial port to connect.
  }
  // Cau hinh FreeRTOS
  xTaskCreate(opendoorTask, "OpenDoorTask", 2048, NULL, 1, NULL);
}

//idea
// void opendoor(string cmd){
//   if cmd == "open"
//   then servo360.write(180) // mở cửa
//   khi chạm cảm biến hành trình thì 
//   servo360.write(90) 
//   dừng lại 12s
//   và gửi tín hiệu uart đến esp32 là cửa đã mở 
//   sau đó đóng cửa 
//   servo360.write(0)
//   nếu cảm biến hồng ngoại phát hiện vật cản lên 1 thì lập tức quay chiều servo360 độ
//   Serial.println(digitalRead(sensor));  
//   servo360.write(180) // mở cửa
//   và đợi tiếp 6s thì đóng 
//   nếu đóng được thì gửi tín hiệu uart là cửa đã đóng.  
// }

static void opendoorTask(void *parameter) {
  for (;;) {
    // Chờ đến khi có lệnh mới
    if (newCommandAvailable && receivedCommand == "open") {
      newCommandAvailable = false;

      // Bắt đầu mở cửa
      servo360.write(180);

      // Đợi đến khi cảm biến hành trình được kích hoạt2
      while (digitalRead(hanhTrinhSensorPin) == LOW) {
        vTaskDelay(10 / portTICK_PERIOD_MS);  // Delay nhẹ để không chiếm CPU
      }

      // Dừng servo
      servo360.write(90);
      vTaskDelay(12000 / portTICK_PERIOD_MS);  // Dừng 12 giây

      // Gửi tín hiệu UART báo cửa đã mở
      Serial.println("CUA_DA_MO");

      // Kiểm tra cảm biến hồng ngoại
      if (digitalRead(infraredsensor) == HIGH) {
        // Có vật cản -> quay ngược lại để mở lại cửa
        servo360.write(180);
        vTaskDelay(6000 / portTICK_PERIOD_MS);

        // Sau đó đóng cửa lại
        servo360.write(0);
        vTaskDelay(2000 / portTICK_PERIOD_MS);

        // Gửi tín hiệu UART báo cửa đã đóng
        Serial.println("CUA_DA_DONG");
      } else {
        // Không có vật cản -> đóng cửa bình thường
        servo360.write(0);
        vTaskDelay(2000 / portTICK_PERIOD_MS);

        // Gửi tín hiệu UART báo cửa đã đóng
        Serial.println("CUA_DA_DONG");
      }
    }

    vTaskDelay(100 / portTICK_PERIOD_MS);  // Kiểm tra lệnh mỗi 100ms
  }
}

void parseCommand(String cmd) {
  if (cmd[0] != '#') return;
  cmd = cmd.substring(1, cmd.length() - 1); // remove '#' and ';'

  int firstComma = cmd.indexOf(',');
  int secondComma = cmd.indexOf(',', firstComma + 1);

  int pan = cmd.substring(0, firstComma).toInt();
  int tilt = cmd.substring(firstComma + 1, secondComma).toInt();
  String servo360Cmd = cmd.substring(secondComma + 1);

  panServo.write(pan);
  tiltServo.write(tilt);

  
}

void loop(){
  // luu bien cap nhat thong tin va gui lai thong tin 
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    Serial.println("Received: " + command);

    Serial.println("DOOR_STATE:OPEN"); // hoặc CLOSED

  }


  while (Serial.available()) {
    char c = Serial.read();
    uartBuffer += c;
    if (c == ';') {
      parseCommand(uartBuffer);
      uartBuffer = "";
    }
  }
  controlpantilt();
}