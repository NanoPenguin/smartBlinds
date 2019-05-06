from time import sleep
import RPi.GPIO as GPIO

class Sound():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        self._pwmPin = GPIO.PWM(13, 800)

    def makeSound(self):
        self._pwmPin.start(0)
        self._pwmPin.ChangeDutyCycle(50)
        for i in range(1,6,1):
            sleep(400)
            self._pwmPin.ChangeFrequency((800+(100*i)))

    def stopSound(self):
        self._pwmPin.stop()

    def gpioCleanup(self):
        GPIO.cleanup()
