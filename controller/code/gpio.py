"""
Class for reading io-inputs on pins
"""

from gpiozero import Button
from gpiozero import LED
import time

class Io():
    def __init__(self):  # initialize GPIO
        self._up = Button(27)
        self._down = Button(22)
        self._left = Button(17)
        self._right = Button(23)

    def waitForInput(self, timeOut=10):
        now = time.time()
        while True:
            if not self._up.is_pressed:
                return 'up'
            elif not self._down.is_pressed:
                return 'down'
            elif not self._left.is_pressed:
                return 'left'
            elif not self._right.is_pressed:
                return 'right'
            time.sleep(0.1)
            then = time.time()
            if then-now>timeOut:
                return False

    def readInput(self):
        if not self._up.is_pressed:
            return 'up'
        elif not self._down.is_pressed:
            return 'down'
        elif not self._left.is_pressed:
            return 'left'
        elif not self._right.is_pressed:
            return 'right'
        return False

    def digitalWrite(self,pinNumber,mode):
        pinOut = LED(pinNumber)
        if mode is 'HIGH':
            pinOut.on()
        else:
            pinOut.off()
