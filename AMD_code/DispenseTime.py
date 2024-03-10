import RPi.GPIO as GPIO
import time
import serial

# Define the serial port
arduino_port = '/dev/ttyACM0'  # Change this to match your Arduino port
arduino_baudrate = 9600  # Make sure this matches the baud rate in your Arduino code

# Initialize serial communication with the Arduino
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

def get_time():
   """
   Returns the current time in HH:MM format
   """
   return time.strftime("%H:%M")
   
def check_time(check_time):
   current_time = get_time()
   if current_time == check_time:
      arduino.write(b'1')  # Send command to Arduino
      

first = "14:26"

check_time(first)

while True:
   check_time(first) 
   time.sleep(60)
