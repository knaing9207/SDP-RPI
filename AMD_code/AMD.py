import RPi.GPIO as GPIO
import time
import serial
from OCR_Text_Extraction import imageocr
import os

# Define the serial port
arduino_port = '/dev/ttyACM0'  # Change this to match your Arduino port
arduino_baudrate = 9600  # Make sure this matches the baud rate in your Arduino code

# Initialize serial communication with the Arduino
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

#def buttons(str1,str2,str3,str4,str5,str6,str7,str8):
# Set up GPIO mode and pins
button1 = 0 #27 
button2 = 1 #28
button3 = 22 #15 0,1,22,23,5,6,16,26
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
print("ready")
while Run:
    
    if GPIO.input(button1) == GPIO.LOW:
        print("Button 1 pressed!")
        arduino.write(b'1')  # Send command to Arduino
        time.sleep(0.2)  # Add a small delay to debounce
        while GPIO.input(button1) == GPIO.LOW:
            time.sleep(0.2)
        time.sleep(0.2)  

    if GPIO.input(button2) == GPIO.LOW:
        LEDs = 25
        GPIO.setup(LEDs, GPIO.OUT)
        print("Button 2 pressed!")
        fswebcam = 'fswebcam --resolution 1920x1080 --save /home/team31/project/AMD_code/image2.jpg'
        GPIO.output(LEDs, GPIO.HIGH)
        os.system(fswebcam)
        arduino.write(b'1')  # Send command to Arduino
        time.sleep(2.5)
        fswebcam = 'fswebcam --resolution 1920x1080 --save /home/team31/project/AMD_code/image3.jpg'
        os.system(fswebcam)
        arduino.write(b'2')
        time.sleep(2.5)
        fswebcam = 'fswebcam --resolution 1920x1080 --save /home/team31/project/AMD_code/image1.jpg'
        os.system(fswebcam)
        time.sleep(5)
        GPIO.output(LEDs, GPIO.LOW)
        GPIO.cleanup(LEDs)
        arduino.write(b'3')
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
        
  