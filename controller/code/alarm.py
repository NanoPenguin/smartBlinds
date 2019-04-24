"""
Class for storing alarms
"""

import time

class Alarm():  # class for each alarm object
    def __init__(self, time, activated=True):
        self._time = time
        self._activated = activated


    def __str__(self):  # formats the time for printing
        return time.ctime(self._time)


    def getTime(self):  # get the set time
        return self._time


    def setTime(self, newTime):  # set a new time
        self._time = newTime


    def isActivated(self):  # get activated True/False
        return self._activated


    def activate(self):  # set activated to True
        self._activated = True


    def deactivate(self):  # set activated to False
        self._activated = False

    def toggleActivated(self): # toggle activated/deactivated
        if self._activated:
            self._activated = False

        else: self._activated = True
