#include <EEPROM.h>

#include <EEPROM.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h> 
#include <LiquidCrystal.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0X27,16,2);


#define RST_PIN         9
#define SS_PIN          10

int diachi_1 = 1, diachi_2 = 5;
byte giatri_1, giatri_2;
int sensor = 2; 
int value;
int servo_1 = 5, servo_2 = 6;
int goc_1, goc_2;
int UID[4], i, RFIDval;
int ID1[4] = {35, 115, 238, 47};
int ID2[4] = {163, 131, 013, 20};

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo myServo_1;
Servo myServo_2;

void setup() 
{
  Serial.begin(9600);
  SPI.begin();
  mfrc522.PCD_Init();

  pinMode(sensor, INPUT);
  
  myServo_1.attach(servo_1);
  myServo_2.attach(servo_2);
  
  lcd.init();
  lcd.backlight();

}

void RFID() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  { 
    return; 
  }
  
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {  
    return;  
  }
  
  Serial.print("UID của thẻ: ");   
  
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  { 
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");   
    UID[i] = mfrc522.uid.uidByte[i];
    Serial.print(UID[i]);
  }

  Serial.println("   ");

  if (UID[i] == ID1[i]) RFIDval = 1;
  else if (UID[i] == ID2[i]) RFIDval = 2;
  else RFIDval = -1;
  
  mfrc522.PICC_HaltA();  
  mfrc522.PCD_StopCrypto1();
}

void loop() {
  EEPROM.write(diachi_1, giatri_1);
  EEPROM.write(diachi_2, giatri_2);
  myServo_1.write(giatri_1);
  myServo_2.write(giatri_2);
  
  RFID();
  if (RFIDval == 1) 
  {
    Serial.println("Open the left door");
    lcd.setCursor(1,0);
    lcd.print("Open");
    lcd.setCursor(3,1);
    lcd.print("the left door");
      
    myServo_1.write(90);
    goc_1 = myServo_1.read();
    goc_2 = myServo_2.read();
    Serial.print("Góc servo 1: "); Serial.println(goc_1);  
    Serial.print("Góc servo 2: "); Serial.println(goc_2);  
    EEPROM.write(diachi_1, goc_1);
    EEPROM.write(diachi_2, goc_2);
    
    delay(15000);
    
  }
  else if (RFIDval == 2) 
  {
    Serial.println("Open 2 doors");
    lcd.setCursor(1,0);
    lcd.print("Open");
    lcd.setCursor(3,1);
    lcd.print("2 doors");
      
    myServo_1.write(90);
    myServo_2.write(90);
    goc_1 = myServo_1.read();
    goc_2 = myServo_2.read();
    Serial.print("Góc servo 1: "); Serial.println(goc_1);  
    Serial.print("Góc servo 2: "); Serial.println(goc_2);  
    EEPROM.write(diachi_1, goc_1);
    EEPROM.write(diachi_2, goc_2);
   
    delay(15000);
    
  } else if (RFIDval == -1) 
  {
    Serial.println("Invalid card");
    lcd.setCursor(1,0);
    lcd.print("Invalid card");
    RFIDval = 0;
  }
  
  if (RFIDval !=0)
  {
    value = digitalRead(sensor);
    if (value == 0 )
    {
      lcd.clear();
      
      myServo_1.write(0);
      myServo_2.write(0); 
      EEPROM.write(diachi_1, goc_1);
      EEPROM.write(diachi_2, goc_2);
    
      RFIDval = 0;
    }
  }
}
