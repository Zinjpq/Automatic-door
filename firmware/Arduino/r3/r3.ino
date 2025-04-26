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
String validCards[] = {
  "A3 83 0D 14",
  "23 73 EE 2F"
};
////////////////////////////////////////////////////////////
// Cau hinh servo
#include "Servo.h"
#define SERVO360_PIN 3
Servo servo360;
enum DoorState { CLOSED, OPEN };
DoorState doorState = CLOSED;
bool isOpening = false;
////////////////////////////////////////////////////////////
// Cau hinh cam bien hong ngoai
#define infraredsensor A2 
// Cam bien hanh trinh
#define positionsensorClose A0  // Cam bien khi dong 
#define positionsensorOpen A1  // Cam bien khi mo
////////////////////////////////////////////////////////////
// Cau hinh cho UART 
#include <Arduino.h>
String uartBuffer = "";
////////////////////////////////////////////////////////////
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
// SDA A4
// SCL A5
 
void setup() {
  Serial.begin(9600);
  ////////////////////////////////////////////////////////////
  // RFID
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init MFRC522
  ////////////////////////////////////////////////////////////
  // Setup servo
  servo360.attach(SERVO360_PIN);
  ////////////////////////////////////////////////////////////
  // Cau hinh chan cam bien
  pinMode(infraredsensor, INPUT);
  pinMode(positionsensorClose,INPUT_PULLUP);
  pinMode(positionsensorOpen, INPUT_PULLUP);
  ////////////////////////////////////////////////////////////
  // khoi tao lcd i2c
  lcd.init();
  lcd.backlight();
  ////////////////////////////////////////////////////////////
  // Quay servo để đóng cửa đến khi chạm cảm biến hành trình đóng
  Serial.println("Initializing: Closing door...");
  lcd.setCursor(0, 0);
  lcd.print("Closing...");
  servo360.write(70);
  // Chờ đến khi cảm biến đóng bị kích hoạt
  while (digitalRead(positionsensorClose) == HIGH) {
    // Đợi cho đến khi cửa đóng hoàn toàn
  }
  // Dừng servo
  servo360.write(90); // 90 là điểm dừng cho servo 360 độ
  delay(500); // Cho servo ổn định
  // Cập nhật trạng thái cửa
  doorState = CLOSED;
  Serial.println("DOOR_STATE: CLOSED");
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Door closed");
}

void loop() {
  if (!rfid.PICC_IsNewCardPresent()) return;
  if (!rfid.PICC_ReadCardSerial()) return;
  String uidStr = getCardUID(rfid.uid);
  Serial.print("Đã quét thẻ: ");
  Serial.println(uidStr);

  if (isValidCard(uidStr) && !isOpening && doorState == CLOSED){
      Serial.println("Thẻ hợp lệ! Gửi lệnh mở cửa.");
      isOpening = true;
      openDoor();
      delay(6000);
      closeDoorWithIRCheck();
      isOpening = false;
  }
  
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 'o' && !isOpening && doorState == CLOSED) {
      isOpening = true;
      openDoor();
      delay(6000);
      closeDoorWithIRCheck();
      isOpening = false;
      command = 'b';
    }
  }

  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}

void openDoor() {
  lcd.clear();
  lcd.print("Opening...");
  servo360.write(110); // quay mở

  while (digitalRead(positionsensorOpen) == HIGH) {
    delay(10); // chờ đến khi chạm công tắc mở
  }

  servo360.write(90); // dừng
  lcd.clear();
  lcd.print("Door opened");
  doorState = OPEN;
  Serial.println("DOOR_STATE: OPEN");
}

void closeDoorWithIRCheck() {
  lcd.clear();
  lcd.print("Closing...");
  servo360.write(70); // quay đóng

  while (digitalRead(positionsensorClose) == HIGH) {
    if (digitalRead(infraredsensor) == LOW) {
      lcd.clear();
      lcd.print("Obstacle!");
      openDoor();           // mở lại
      delay(3000);          // đợi 3s
      lcd.clear();
      lcd.print("Retry close");
      servo360.write(70);      // thử đóng lại
    }
    delay(10);
  }

  servo360.write(90); // dừng
  lcd.clear();
  lcd.print("Door closed");
  doorState = CLOSED;
  Serial.println("DOOR_STATE: CLOSED");
}

String getCardUID(MFRC522::Uid uid) {
  String uidStr = "";
  for (byte i = 0; i < uid.size; i++) {
    if (uid.uidByte[i] < 0x10) uidStr += "0"; // thêm số 0 nếu < 0x10
    uidStr += String(uid.uidByte[i], HEX);
    if (i < uid.size - 1) uidStr += " ";
  }
  uidStr.toUpperCase(); // viết hoa để khớp
  return uidStr;
}

bool isValidCard(String uidStr) {
  for (String card : validCards) {
    if (uidStr == card) return true;
  }
  return false;
}