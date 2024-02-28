#include <SPI.h>
#include <Servo.h>

Servo servo1;
int angle1 = 0;

void setup() {
    Serial.begin(9600);
    start(8, servo1);

}

void loop() {
  
    // Additional setup code for your e-paper display
    if (Serial.available() > 0) {
      
        char command = Serial.read();
        
        if (command == '1') {
            
          dispense(servo1, angle1);
          
        }
        
    }
}

void start(int pin, Servo &myservo) { 
  myservo.attach(pin);
  myservo.write(0);
}

void dispense(Servo &servo, int &angle) { 
  // scan from 0 to 180 degrees
  for(angle = 0; angle < 180; angle++) {                                  
    servo.write(angle);               
    delay(10);                   
  } 
  // now scan back from 180 to 0 degrees
  for(angle = 180; angle > 0; angle--) {                                
    servo.write(angle);           
    delay(15);       
  } 
}
