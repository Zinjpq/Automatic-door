#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <LiquidCrystal_I2C.h>
#include <MFRC522.h>
#include <SPI.h>

// I2C addresses
#define I2C_LCD_ADDRESS 0x27
#define PCA9685_ADDRESS 0x40

// RFID pins
#define RFID_SS_PIN 5
#define RFID_RST_PIN 4

// Servo Driver
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(PCA9685_ADDRESS);

// LCD
LiquidCrystal_I2C lcd(I2C_LCD_ADDRESS, 16, 2);

// RFID
MFRC522 mfrc522(RFID_SS_PIN, RFID_RST_PIN);

void setup() {
  Serial.begin(115200);

  // Initialize I2C bus
  Wire.begin();

  // Initialize LCD
  lcd.begin();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Hello, World!");

  // Initialize PWM Servo Driver
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz

  // Initialize RFID
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522

  // Initialize LM393 sensor pin
  pinMode(14, INPUT);
}

void loop() {
  // Code to control servos
  int servo1Angle = 150; // Example angle
  int servo2Angle = 300; // Example angle
  pwm.setPWM(0, 0, servo1Angle);
  pwm.setPWM(1, 0, servo2Angle);

  // Code to read RFID
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.println("RFID card detected!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("RFID detected!");

    // Print RFID card UID
    Serial.print("UID: ");
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
    }
    Serial.println();

    mfrc522.PICC_HaltA(); // Stop reading
  }

  // Code to read LM393 sensor
  int sensorValue = digitalRead(14);
  Serial.print("LM393 sensor value: ");
  Serial.println(sensorValue);

  delay(1000);
}
