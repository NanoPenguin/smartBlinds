"""
Class for storing alarms
"""

class Alarm(self, time, activated=true):  # class for each alarm object
    def __init__(self, time, activated):
        self.__time = time
        self.__activated = activated


    def getTime(self):  # get the set time
        return self.__time


    def setTime(self, newTime):  # set a new time
        self.__time = newTime


    def isActivated(self):  # get activated True/False
        return self.__activated


    def activate(self):  # set activated to True
        self.__activated = True


    def deactivate(self):  # set activated to False
        self.__activated = False

    def toggleActivated(self): # toggle activated/deactivated
        if self.__activated:
            self.__activated = False

        else: self.__activated = True
