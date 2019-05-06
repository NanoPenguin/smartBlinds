"""
Class for reading io-inputs on pins
"""

from gpiozero import Button
from time import sleep

class Gpio():
    def __init__(self):
        self._up = Button(17)
        self._down = Button(27)
        self._left = Button(22)
        self._right = Button(23)


    def waitForInput(self):
        while True:
            if self._up.is_pressed:
                return 'up'
            elif self._down.is_pressed:
                return 'down'
            elif self._left.is_pressed:
                return 'left'
            elif self._right.is_pressed:
                return 'right'
            sleep(0.1)
