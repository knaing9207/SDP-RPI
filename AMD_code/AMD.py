import RPi.GPIO as GPIO
import time
import serial
from OCR_Text_Extraction import imageocr


ser = serial.Serial('/dev/ttyACM0', 9600)  # Use the correct serial port

#def buttons(str1,str2,str3,str4,str5,str6,str7,str8):
# Set up GPIO mode and pins
button1 = 0 #27 
button2 = 1 #28
button3 = 22 #15
button4 = 23 #16
button5 = 5 #29
button6 = 6 #31
button7 = 16 #36
button8 = 26 #37

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button8, GPIO.IN, pull_up_down=GPIO.PUD_UP)


Run = True
while Run:
    
    if GPIO.input(button1) == GPIO.LOW:
        print("Button 1 pressed!")
        ser.write(b'1')  # Send command to Arduino
        time.sleep(0.2)  # Add a small delay to debounce
        while GPIO.input(button1) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)  

    if GPIO.input(button2) == GPIO.LOW:
        print("Button 2 pressed!")
        ser.write(b'2')  # Send command to Arduino
        time.sleep(0.2)  # Add a small delay to debounce
        while GPIO.input(button2) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)

    if GPIO.input(button3) == GPIO.LOW:
        print("Button 3 pressed!")
        ###
        while GPIO.input(button3) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)

    if GPIO.input(button4) == GPIO.LOW: ### DISPENSE ###
        print("Button 4 pressed!")
        ###
        while GPIO.input(button4) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)
        
    if GPIO.input(button5) == GPIO.LOW:
        print("Button 5 pressed!")
        ###
        while GPIO.input(button5) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)
        
    if GPIO.input(button6) == GPIO.LOW:
        print("Button 6 pressed!")
        ###
        while GPIO.input(button6) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)
        
    if GPIO.input(button7) == GPIO.LOW:
        print("Button 7 pressed!")
        ###
        imageocr()
        while GPIO.input(button7) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)
        
    if GPIO.input(button8) == GPIO.LOW:
        print("Button 8 pressed!")
        ###
        while GPIO.input(button8) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)
        
  