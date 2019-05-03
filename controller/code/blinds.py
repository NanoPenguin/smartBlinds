"""
Class for the state of the blinds
ANGLE:
UP: angle = 300
DOWN: angle = 0
"""

class Blinds():
    def __init__(self, angle):  # initialize blinds object
        self._angle = angle
        self._upAngle = 300
        self._openAngle = 150
        self._downAngle = 0


    def getAngle(self):  # return current angle
        return self._angle


    def setAngle(self, angle):  # set new angle
        self._angle = angle


    def Up(self):  # set blinds to up
        self.setAngle(self._upAngle)


    def Down(self):  # set blinds to down
        self.setAngle(self._downAngle)


    def Open(self):  # set blinds to open
        self.setAngle(self._openAngle)
