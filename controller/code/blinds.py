"""
Class for the state of the blinds
"""

from communication import *


class Blinds():
    def __init__(self, angle = 600):
        self._angle = angle
        self._time = 0
        self._downAngle = 1023
        self._openAngle = 600
        self._upAngle = 0
        self._blinds = Communication()
        if self.getBlindsData()[0] == self._openAngle:
            self._state = "open"
        else:
            self._state = "closed"

    def getState(self):
        return self._state

    # get the setpoint and position
    def getBlindsData(self):  # return current angle
        try:
            setpoint, position = self._blinds.getBlindsData()
            return setpoint, position
        except AttributeError:
            print("No blinds connected")
            return 0, 0


    # set blinds to angle
    def setAngle(self, angle, time = 0):  # set new angle
        self._angle = angle
        self._time = time
        try:
            self._blinds.setBlinds(self._angle, self._time)
            return True
        except AttributeError:
            print("No blinds connected")
            return False


    # open blinds in the up-position
    def up(self):  # set blinds to up
        self._state = "closed"
        return self.setAngle(self._upAngle)


    # open blinds in the down-position
    def down(self):  # set blinds to down
        self._state = "closed"
        return self.setAngle(self._downAngle)


    # open blinds horizontally
    def open(self):  # set blinds to open
        self._state = "open"
        return self.setAngle(self._openAngle)
