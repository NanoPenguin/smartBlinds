"""
Class for reading io-inputs on pins
"""

from gpiozero import Button
import time

INPUTTIMEOUT = 10

class Io():
    def __init__(self):  # initialize GPIO
        self._up = Button(27)
        self._down = Button(22)
        self._left = Button(17)
        self._right = Button(23)


    def waitForInput(self):
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
            if then-now>INPUTTIMEOUT:
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
