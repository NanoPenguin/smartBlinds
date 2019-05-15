"""
Class for the state of the blinds
"""
from communication import *

class Blinds():
    def __init__(self, angle = 600):  # initialize blinds object
        self._angle = angle
        self._time = 0
        self._downAngle = 1023
        self._openAngle = 600
        self._upAngle = 0
        self._blinds = Communication()


    def getBlindsData(self):  # return current angle
        try:
            setpoint, position = self._blinds.getBlindsData()
            return setpoint, position
        except AttributeError:
            print("No blinds connected")
            return 0, 0


    def setAngle(self, angle, time = 0):  # set new angle
        self._angle = angle
        try:
            self._blinds.setBlinds(self._angle, self._time)
            return True
        except AttributeError:
            print("No blinds connected")
            return False


    def up(self):  # set blinds to up
        return self.setAngle(self._upAngle)


    def down(self):  # set blinds to down
        return self.setAngle(self._downAngle)

    def open(self):  # set blinds to open
        return self.setAngle(self._openAngle)
