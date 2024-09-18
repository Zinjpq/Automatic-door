#include <WiFi.h>
#include <ESP32Servo.h>

// Servo object instances
Servo panServo;
Servo tiltServo;

// Define pins
#define PAN_PIN 12
#define TILT_PIN 13

// Servo angle limits
#define MIN_ANGLE 0
#define MAX_ANGLE 180

// Starting positions for servos
int panAngle = 90;   // Start pan at center
int tiltAngle = 90;  // Start tilt at center

// Step size for each movement
const int stepSize = 10; 

void setup_servo(){
  // Attach servos to their pins
  panServo.attach(PAN_PIN);
  tiltServo.attach(TILT_PIN);

  // Move servos to the starting position
  panServo.write(panAngle);
  tiltServo.write(tiltAngle);

  server.on("/left", g_l);
  server.on("/right", g_r);
  server.on("/up", g_u);
  server.on("down", g_d);
}

void g_l(){
  panAngle = max(panAngle - stepSize, MIN_ANGLE);  // Move left, ensure within bounds
  panServo.write(panAngle);
}

void g_r(){
  panAngle = max(panAngle + stepSize, MIN_ANGLE);  // Move left, ensure within bounds
  panServo.write(panAngle);
}

void g_u(){
  tiltAngle = max(tiltAngle - stepSize, MIN_ANGLE);  // Move left, ensure within bounds
  tiltServo.write(tiltAngle);
}

void g_d(){
  tiltAngle = max(tiltAngle + stepSize, MIN_ANGLE);  // Move left, ensure within bounds
  tiltServo.write(tiltAngle);
}
