import os
import RPi.GPIO as GPIO
import time

while True:
    user = input("Take Picture?: (yes/no) ")
    if user == "y":
        GPIO.setmode(GPIO.BCM)
        LEDs = 25
        GPIO.setup(LEDs, GPIO.OUT)

        GPIO.output(LEDs, GPIO.HIGH)
        time.sleep(2)
        fswebcam = 'fswebcam --resolution 1920x1080 --set "Focus, Automatic Continuous"=False --set "Focus, Absolute"=300 --crop 1000x1080+460+0 --save /home/team31/project/AMD_code/image.jpg'

        os.system(fswebcam)

        time.sleep(5)
        GPIO.output(LEDs, GPIO.LOW)
        GPIO.cleanup(LEDs)
