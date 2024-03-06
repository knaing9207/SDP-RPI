#include <SPI.h>
#include <Servo.h>

Servo servo1;
int angle1 = 0;
int photoPin1 = A0;
bool state1;

void setup() {
  start(8, servo1);
  delay(1000);
}

void loop() {
  
    // Additional setup code for your e-paper display
    if (Serial.available() > 0) {
      
        char command = Serial.read();
        
        if (command == '1') {
            
          dispenseAndDetect(servo1, angle1, state1, photoPin1);
          
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
      if (light < 90) {
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
      if (light < 90) {
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
