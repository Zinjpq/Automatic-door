#include <WiFi.h>
#include <ESP32Servo.h>

int panAngle, tiltAngle;

#define stepSize 10
#define MIN_ANGLE 0
#define MAX_ANGLE 180

// Servo object instances
Servo panServo;
Servo tiltServo;

// Define pins
#define PAN_PIN 12
#define TILT_PIN 13

// // Functions to move the servos
// void go_left(){
//   panAngle = min(panAngle - stepSize, MIN_ANGLE);  
//   panServo.write(panAngle);
// }

// void go_right(){
//   panAngle = max(panAngle + stepSize, MAX_ANGLE);  
//   panServo.write(panAngle);
// }

// void go_up(){
//   tiltAngle = min(tiltAngle - stepSize, MIN_ANGLE);
//   tiltServo.write(tiltAngle);
// }

// void go_down(){
//   tiltAngle = max(tiltAngle + stepSize, MAX_ANGLE);
//   tiltServo.write(tiltAngle);
// }

void setup_2servo(){
  // Attach servos to their pins
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);

  panAngle = 90;
  tiltAngle = 90;

  // Move servos to the starting position
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);

  // Correct usage of server.on by passing function pointers
  server.on("/left", panServo.write(min(panAngle - stepSize, MIN_ANGLE)));
  server.on("/right", panServo.write(max(panAngle + stepSize, MAX_ANGLE)));
  server.on("/up",tiltServo.write(min(tiltAngle - stepSize, MIN_ANGLE)));
  server.on("/down", tiltServo.write(max(tiltAngle + stepSize, MAX_ANGLE));
}
