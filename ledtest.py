 #!/usr/bin/python
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
while True:
    GPIO.output(3, True)
    time.sleep(2)
    GPIO.output(3, False)
    time.sleep(1)
