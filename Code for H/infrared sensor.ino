int cambien = 5; //Chân cảm biến nối chân số 5 Arduino
int giatri;

void setup() {
  Serial.begin(9600);
  pinMode(cambien, INPUT);
}

void loop() {
  giatri = digitalRead(cambien); //Đọc giá trị digital từ cảm biến và gán vào biến giatri

  Serial.print("Giá trị cảm biến là: ");
  Serial.println(giatri);
  delay(200);
}
