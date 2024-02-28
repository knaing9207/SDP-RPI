import RPi.GPIO as GPIO
import time

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Set PWM pin
pwm_pin = 12

# Set PWM frequency
frequency = 50  # Hz

# Initialize PWM
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, frequency)

2.5
5
7.5
10
12.5

try:
    # Start PWM with duty cycle for 0 degrees
    pwm.start(7.5)
    time.sleep(2)  # Wait for the servo to reach the position
    pwm.start(2.5)
    time.sleep(2)  # Wait for the servo to reach the position
    pwm.start(12.5)
    time.sleep(2)  # Wait for the servo to reach the position
    pwm.start(7.5)
    time.sleep(2)  # Wait for the servo to reach the position
    


except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C exit
    pwm.stop()
    GPIO.cleanup()