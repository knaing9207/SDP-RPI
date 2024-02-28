import RPi.GPIO as GPIO
import time

# Set up GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Set pin 17 as output
led_pin = 25
GPIO.setup(led_pin, GPIO.OUT)

try:
    while True:
        # # Turn the LED on
        GPIO.output(led_pin, GPIO.HIGH)
        print("LED on")
        time.sleep(1)  # Delay for 1 second

        # Turn the LED off
        GPIO.output(led_pin, GPIO.LOW)
        print("LED off")
        time.sleep(1)  # Delay for 1 second

except KeyboardInterrupt:
    # Clean up GPIO
    GPIO.cleanup()
