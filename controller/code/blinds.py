"""
Class for the state of the blinds
UP: state = True
DOWN: state = False

ANGLE:
CLOSED-UP: angle = 1
OPEN: angle = 0
CLOSED-DOWN: angle = -1
"""

class Blinds():
    def __init__(self, state, angle):  # initialize blinds object
        self.__state = state
        self.__angle = angle


    def getState(self):  # return current state
        return self.__state


    def setState(self, state):  # set new state
        self.__state = state


    def getAngle(self):  # return current angle
        return self.__angle


    def setAngle(self, angle):  # set new angle
        self.__angle = angle
