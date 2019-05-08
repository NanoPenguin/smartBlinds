"""
Class for storing alarms
"""

import time

class Alarm():  # class for each alarm object
    def __init__(self, time, fromCalendar=False, activated=True):
        self._time = time
        self._fromCalendar = fromCalendar
        self._activated = activated


    def __str__(self):  # formats the time for printing
        return time.strftime("%H:%M", time.localtime(self._time))


    def getTime(self):  # get the set time
        return self._time


    def setTime(self, newTime):  # set a new time
        self._time = newTime


    def isActivated(self):  # get activated True/False
        return self._activated


    def isFromCalendar(self):
        return self._fromCalendar


    def getHour(self):
        hour = int(time.strftime("%H", time.localtime(self._time)))
        return hour


    def getMinute(self):
        minute = int(time.strftime("%M", time.localtime(self._time)))
        return minute


    def activate(self):  # set activated to True
        self._activated = True


    def deactivate(self):  # set activated to False
        self._activated = False


    def toggleActivated(self): # toggle activated/deactivated
        if self._activated:
            self._activated = False

        else: self._activated = True


    def savingStr(self):
        return str(int(self._time))+','+str(self._fromCalendar)+','+str(self._activated)

    def printingStr(self):
        active = ' Inactive'
        if self._activated:
            active = ' Active'
        fromCal = ''
        if self._fromCalendar:
            fromCal = ' from calendar'
        return str(str(self)+active+fromCal)
