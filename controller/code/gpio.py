"""
Class for reading io-inputs on pins
"""

from gpiozero import Button
from time import sleep

class Io():
    def __init__(self):  # initialize GPIO
        self._up = Button(17)
        self._down = Button(23)
        self._left = Button(22)
        self._right = Button(27)


    def waitForInput(self):
        while True:
            if not self._up.is_pressed:
                return 'up'
            elif not self._down.is_pressed:
                return 'down'
            elif not self._left.is_pressed:
                return 'left'
            elif not self._right.is_pressed:
                return 'right'
            sleep(0.1)
