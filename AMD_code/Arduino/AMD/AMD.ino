#include <SPI.h>
#include <Servo.h>

// Dispenser
Servo servo1;
int angle1 = 0;
int photoPin1 = A0;
bool state1;

// Bottle Stand
Servo servoMotor; // Create a servo object
const int servoPin = 9; // Set the servo pin

void setup() {

  // Dispenser
  Serial.begin(9600);
  start(8, servo1);
  delay(1000);

  // Bottle Stand
  servoMotor.attach(servoPin); // Attach the servo to the pin
  servoMotor.write(90); // Initialization position
}

void loop() {
  
    if (Serial.available() > 0) {
      
        char command = Serial.read();
        
        if (command == '1') {
          // Dispense
          dispenseAndDetect(servo1, angle1, state1, photoPin1);
          
        }
        else if (command == '2') {
            
          // Rotate slowly to the ending position
          for (int angle = 90; angle >= 70; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (command == '3') {
            
          // Rotate slowly to the ending position
          for (int angle = 70; angle >= 50; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (command == '4') {
            
          // Rotate slowly to the ending position
          for (int angle = 50; angle >= 30; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
          
        }
        else if (command == '5') {
            
          // Rotate slowly back to the starting position
          for (int angle = 30; angle <= 110; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (command == '6') {
            
          // Rotate slowly back to the starting position
          for (int angle = 110; angle <= 130; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (command == '7') {
            
          // Rotate slowly back to the starting position
          for (int angle = 130; angle <= 150; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (command == '8') {
            
           // Rotate slowly back to the starting position
          for (int angle = 150; angle >= 90; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
    }
}

void start(int pin, Servo &myservo) {
  myservo.attach(pin);
  myservo.write(0);
}

void dispenseAndDetect(Servo &servo, int &angle, bool &state, int photoPin) {
  state = false;
  while (!state) {
    // Dispensing process with interspersed light sensing
    for (angle = 0; angle < 180; angle++) {
      servo.write(angle);
      delay(10);
      // Check light level during dispensing
      int light = analogRead(photoPin);
      if (light < 50) {
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
      if (light < 50) {
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
