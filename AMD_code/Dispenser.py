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
        self.pwm.ChangeDutyCycle(0)

        # Piezo Speaker
        GPIO.setup(18, GPIO.OUT)
        self.speaker = GPIO.PWM(18, 100)

    def dispense(self):
        self.pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(3.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(12.5)
        time.sleep(1)
        self.pwm.ChangeDutyCycle(0)
        self.dispenser.quantity =- 1

        # Piezo Speaker
        self.speaker.start(50)
        GPIO.output(18, GPIO.HIGH)
        self.speaker.ChangeFrequency(261.63) # C4
        time.sleep(0.5)
        self.speaker.ChangeFrequency(523.25) # A5
        time.sleep(0.5)
        self.speaker.ChangeFrequency(261.63) # C4
        time.sleep(0.5)
        self.speaker.ChangeFrequency(523.25) # A5
        time.sleep(0.5)
        self.speaker.ChangeDutyCycle(0)
        time.sleep(0.5)
        GPIO.output(18, GPIO.LOW)
        

# p1 = Dispenser(1, 13)
# p1.dispense()
# time.sleep(1)