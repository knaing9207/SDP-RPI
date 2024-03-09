import serial
import time

# Define the serial port
arduino_port = '/dev/ttyACM0'  # Change this to match your Arduino port
arduino_baudrate = 9600  # Make sure this matches the baud rate in your Arduino code

# Initialize serial communication with the Arduino
arduino = serial.Serial(arduino_port, arduino_baudrate, timeout=1)

# Wait for Arduino to initialize
time.sleep(2)

# Send commands to Arduino
while True:
    arduino.write(b'1')  # Send 'on' command to Arduino
    time.sleep(1)  # Wait for 1 second
    arduino.write(b'2')  # Send 'off' command to Arduino
    time.sleep(1)  # Wait for 1 second