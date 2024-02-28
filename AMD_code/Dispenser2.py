import RPi.GPIO as GPIO
import time
from Pill_Info import pillinfo

class Dispenser():
    def __init__(self, id, servoPIN) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servoPIN, GPIO.OUT)
        self.dispenser = pillinfo(id)
        self.pwm = GPIO.PWM(servoPIN, 50)
        self.pwm.start(12.5) # Initialization

    def dispense_slowly(self):
        # Rotate slowly to the starting position
        for duty_cycle in range(120, 20, -5):
            self.pwm.ChangeDutyCycle(duty_cycle/10)
            time.sleep(0.1)

        # Pause at the starting position
        time.sleep(1)

        # Rotate slowly to the ending position
        for duty_cycle in range(20, 130,5):
            self.pwm.ChangeDutyCycle(duty_cycle/10)
            time.sleep(0.1)

        # Pause at the ending position
        time.sleep(1)

        # Set the servo to a neutral position
        self.pwm.ChangeDutyCycle(0)

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

# Create an instance of the Dispenser class
p1 = Dispenser(1, 13)

try:
    # Dispense slowly
    p1.dispense_slowly()

finally:
    # Cleanup GPIO on script exit
    p1.cleanup()