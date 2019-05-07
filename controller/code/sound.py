from time import sleep
import RPi.GPIO as GPIO

class Sound():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        self._freq = 500
        self._pwmPin = GPIO.PWM(13, self._freq)

    def makeSound(self):
        self._pwmPin.start(0)
        self._pwmPin.ChangeDutyCycle(100)
        for i in range(10):
            sleep(0.4)
            if i%2==0:
                self._pwmPin.ChangeDutyCycle(0)
            else:
                self._pwmPin.ChangeDutyCycle(100)
        self.stopSound()

    def getFreq(self): # get frequency
        return self._freq

    def stopSound(self):
        self._pwmPin.stop()

    def gpioCleanup(self):
        GPIO.cleanup()

    def increaseFreq(self):
        self._pwmPin.start(0)
        self._pwmPin.ChangeDutyCycle(100)
        for i in range(6):
            sleep(0.8)
            if i%2==0:
                self._pwmPin.ChangeDutyCycle(0)
            else:
                self._pwmPin.ChangeDutyCycle(100)
        self.stopSound()
"""
    def increaseFreq(self):
        self._freq += 100
        self.updateFreq()
"""

    def decreaseFreq(self):
        self._pwmPin.start(0)
        self._pwmPin.ChangeDutyCycle(100)
        sleep(0.1)
        self.stopSound()

    def updateFreq(self):
        self._pwmPin.ChangeFrequency(self._freq)
