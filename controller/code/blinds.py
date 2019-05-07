"""
Class for the state of the blinds
"""
from communication import *

class Blinds():
    def __init__(self, angle = 600):  # initialize blinds object
        self._angle = angle
        self._downAngle = 1023
        self._openAngle = 600
        self._upAngle = 0
        self._blinds = Communication()

    def getBlindsData(self):  # return current angle
        setpoint, position = self._blinds.getBlindsData()
        
        return setpoint, position

    def setAngle(self, angle):  # set new angle
        self._angle = angle
        self._blinds.setBlinds(angle)

    def up(self):  # set blinds to up
        self.setAngle(self._upAngle)


    def down(self):  # set blinds to down
        self.setAngle(self._downAngle)


    def open(self):  # set blinds to open
        self.setAngle(self._openAngle)
