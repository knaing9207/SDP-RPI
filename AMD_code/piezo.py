
import RPi.GPIO as GPIO
from time import sleep
 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pin7 = GPIO.PWM(18, 100)
pin7.start(50)
 
#while True:
  #GPIO.output(18, GPIO.HIGH)
  # pin7.ChangeFrequency(16.35) # C0
  # sleep(1)
  #pin7.ChangeFrequency(261.63) # C4
  #sleep(1)
  # pin7.ChangeFrequency(293.66) # D4
  # sleep(1)
  # pin7.ChangeFrequency(329.63) # E4
  # sleep(1)
  # pin7.ChangeFrequency(349.23) # F4
  # sleep(1)
  # pin7.ChangeFrequency(392.00) # G4
  # sleep(1)
  # pin7.ChangeFrequency(440.00) # A4
  # sleep(1)
  # pin7.ChangeFrequency(493.88) # B4
  # sleep(1)
  #pin7.ChangeFrequency(523.25) # A5
  #sleep(1)
  # pin7.ChangeFrequency(16.35) # C0
  # sleep(1)
  #GPIO.output(18, GPIO.LOW)
  #sleep(1)

GPIO.output(18, GPIO.HIGH)
pin7.ChangeFrequency(261.63) # C4
sleep(1)
pin7.ChangeFrequency(523.25) # A5
sleep(1)
pin7.ChangeFrequency(261.63) # C4
sleep(1)
pin7.ChangeFrequency(523.25) # A5
sleep(1)
pin7.ChangeFrequency(261.63) # C4
sleep(1)
pin7.ChangeFrequency(523.25) # A5
sleep(1)
GPIO.output(18, GPIO.LOW)
sleep(1)