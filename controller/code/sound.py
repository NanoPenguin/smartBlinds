from time import sleep
import RPi.GPIO as GPIO

class Sound():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        self._freq = 800
        self._pwmPin = GPIO.PWM(13, self._freq)

    def makeSound(self):
        self._pwmPin.start(0)
        self._pwmPin.ChangeDutyCycle(50)
        freqTemp = self._freq
        for i in range(5):
            sleep(400)
            self._freq = (self._freq+(100))
            self.updateFreq()
        self._freq = freqTemp
        self.updateFreq()

    def getFreq(self): # get frequency
        return self._freq

    def stopSound(self):
        self._pwmPin.stop()

    def gpioCleanup(self):
        GPIO.cleanup()

    def increaseFreq(self):
        self._freq += 100
        self.updateFreq()

    def decreaseFreq(self):
        self._freq -= 100
        self.updateFreq()

    def updateFreq():
        self._pwmPin.ChangeFrequency(self._freq)
