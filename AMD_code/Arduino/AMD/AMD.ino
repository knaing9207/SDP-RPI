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
      
        String receivedString = Serial.readStringUntil('\n');  // Read the string until newline character
        
        if (receivedString == "Dispense 1") {
          // Dispense
          dispenseAndDetect(servo1, angle1, state1, photoPin1);
          Serial.println("Done 1");
        }
        else if (receivedString == "Dispense 2") {
          // Dispense
          //dispenseAndDetect(servo2, angle2, state2, photoPin2);
        }
        else if (receivedString == "Dispense 3") {
          // Dispense
          //dispenseAndDetect(servo3, angle3, state3, photoPin3);
        }
        else if (receivedString == "Dispense 4") {
          // Dispense
          //dispenseAndDetect(servo4, angle4, state4, photoPin4);
        }
        else if (receivedString == "Pic 1") {
            
          // Rotate slowly to the ending position
          for (int angle = 90; angle >= 70; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (receivedString == "Pic 2") {
            
          // Rotate slowly to the ending position
          for (int angle = 70; angle >= 50; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (receivedString == "Pic 3") {
            
          // Rotate slowly to the ending position
          for (int angle = 50; angle >= 30; angle=angle-5) {
            servoMotor.write(angle);
            delay(100);
          }
          
        }
        else if (receivedString == "Pic 4") {
            
          // Rotate slowly back to the starting position
          for (int angle = 30; angle <= 110; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (receivedString == "Pic 5") {
            
          // Rotate slowly back to the starting position
          for (int angle = 110; angle <= 130; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (receivedString == "Pic 6") {
            
          // Rotate slowly back to the starting position
          for (int angle = 130; angle <= 150; angle=angle+5) {
            servoMotor.write(angle);
            delay(100);
          }
        }
        else if (receivedString == "Pic 7") {
            
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
