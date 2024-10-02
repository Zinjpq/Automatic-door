#include <EEPROM.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h> 
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// Constants and object definitions
#define RST_PIN 9
#define SS_PIN 10
#define SERVO_OPEN_ANGLE 90
#define SERVO_CLOSED_ANGLE 0
#define DELAY_TIME 15000

LiquidCrystal_I2C lcd(0x27, 16, 2);
MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servo1, servo2;

int diachi_1 = 1, diachi_2 = 5;

//Sensor
int sensorPin = 2;

//RFID
int RFIDval = 0;
int UID[4];

//ID 
const int ID1[4] = {35, 115, 238, 47};
const int ID2[4] = {163, 131, 13, 20};

// Setup function
void setup() {
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();
  
  pinMode(sensorPin, INPUT);
  servo1.attach(5);
  servo2.attach(6);
  
  lcd.init();
  lcd.backlight();
}

// Function to check RFID
void checkRFID(){
  if (!mfrc522.PICC_IsNewCardPresent() || !mfrc522.PICC_ReadCardSerial()) return;
  
  for (byte i = 0; i < mfrc522.uid.size; i++) UID[i] = mfrc522.uid.uidByte[i];
  
  RFIDval = (memcmp(UID, ID1, 4) == 0) ? 1 : (memcmp(UID, ID2, 4) == 0) ? 2 : -1;
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
}

// Function to open servos and display message
void openDoor(int mode){
  const char* message = (mode == 1) ? "the left door" : "2 doors";
  Serial.print("Open "); Serial.println(message);
  
  lcd.clear();
  lcd.setCursor(1, 0);
  lcd.print("Open");
  lcd.setCursor(3, 1);
  lcd.print(message);
  
  servo1.write(SERVO_OPEN_ANGLE);
  if (mode == 2) servo2.write(SERVO_OPEN_ANGLE);

  saveServoPositions();
  delay(DELAY_TIME);
}

// Save servo positions to EEPROM
void saveServoPositions(){
  EEPROM.write(diachi_1, servo1.read());
  EEPROM.write(diachi_2, servo2.read());
}

// Main loop function
void loop(){
  checkRFID();

  if (RFIDval > 0) openDoor(RFIDval);
  else if (RFIDval == -1) {
    Serial.println("Invalid card");
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("Invalid card");
    RFIDval = 0;
  }

  if (RFIDval != 0 && digitalRead(sensorPin) == LOW) {
    lcd.clear();
    servo1.write(SERVO_CLOSED_ANGLE);
    servo2.write(SERVO_CLOSED_ANGLE);
    saveServoPositions();
    RFIDval = 0;
  }
}
