#include <SPI.h>
#include <Servo.h>

// Dispenser
Servo servo1;
int angle1 = 0;
int photoPin1 = A0;
bool state1;

Servo servo2;
int angle2 = 0;
int photoPin2 = A1;
bool state2;

Servo servo3;
int angle3 = 0;
int photoPin3 = A2;
bool state3;

Servo servo4;
int angle4 = 0;
int photoPin4 = A3;
bool state4;

// Bottle Stand
Servo servoMotor; // Create a servo object
const int servoPin = 12; // Set the servo pin

void setup() {

  // Dispenser
  Serial.begin(9600);
  start(8, servo1);
  start(9, servo2);
  start(10, servo3);
  start(11, servo4);
  delay(1000);

  // Bottle Stand
  servoMotor.attach(servoPin); // Attach the servo to the pin
  servoMotor.write(90); // Initialization position

//  dispenseAndDetectBlack(servo1, angle1, state1, photoPin1);
//  dispenseAndDetectWhite(servo2, angle2, state2, photoPin2);
//  dispenseAndDetectWhite(servo3, angle3, state3, photoPin3);
//  dispenseAndDetectWhite(servo4, angle4, state4, photoPin4);
}

void loop() {
}

void start(int pin, Servo &myservo) {
  myservo.attach(pin);
  myservo.write(0);
}

void dispenseAndDetectBlack(Servo &servo, int &angle, bool &state, int photoPin) {
  state = false;
  while (!state) {
    // Dispensing process with interspersed light sensing
    for (angle = 0; angle < 180; angle++) {
      servo.write(angle);
      delay(10);
      // Check light level during dispensing
      int light = analogRead(photoPin);
      Serial.println(light); // Print the light intensity to the serial monitor
      if (light < 200) {
        state = true;
        break;
      }
    }
    // If the pill is detected during the forward movement, exit the loop
    if (state) {
      break;
    }

    // now scan back from 180 to 0 degrees
    for (angle = 180; angle > 0; angle--) {
      servo.write(angle);
      delay(15);
      // Check light level during dispensing
      int light = analogRead(photoPin);
      Serial.println(light); // Print the light intensity to the serial monitor
      if (light < 200) {
        state = true;
        break;
      }
    }
    // If the pill is detected during the backward movement, exit the loop
    if (state) {
      break;
    }
  }
}

void dispenseAndDetectWhite(Servo &servo, int &angle, bool &state, int photoPin) {
  state = false;
  while (!state) {
    // Dispensing process with interspersed light sensing
    for (angle = 0; angle < 180; angle++) {
      servo.write(angle);
      delay(10);
      // Check light level during dispensing
      int light = analogRead(photoPin);
      Serial.println(light); // Print the light intensity to the serial monitor
      if (light < 400) {
        state = true;
        break;
      }
    }
    // If the pill is detected during the forward movement, exit the loop
    if (state) {
      break;
    }

    // now scan back from 180 to 0 degrees
    for (angle = 180; angle > 0; angle--) {
      servo.write(angle);
      delay(15);
      // Check light level during dispensing
      int light = analogRead(photoPin);
      Serial.println(light); // Print the light intensity to the serial monitor
      if (light < 400) {
        state = true;
        break;
      }
    }
    // If the pill is detected during the backward movement, exit the loop
    if (state) {
      break;
    }
  }
}
