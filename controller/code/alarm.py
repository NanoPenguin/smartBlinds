"""
Class for storing alarms
"""

import time


class Alarm():
    def __init__(self, time, fromCalendar=False, activated=True):
        self._time = time
        self._fromCalendar = fromCalendar
        self._activated = activated


    # formats the time for printing
    def __str__(self):
        return time.strftime("%H:%M", time.localtime(self._time))

    def __gt__(self, other):
        self._time > other._time

    def __lt__(self, other):
        self._time < other._time

    # get the set time
    def getTime(self):
        return self._time


    # set a new time
    def setTime(self, newTime):
        self._time = newTime


     # get if alarm is activated
    def isActivated(self):
        return self._activated


    # get if alarm is from calendar
    def isFromCalendar(self):
        return self._fromCalendar


    # get the hour for the alarm
    def getHour(self):
        hour = int(time.strftime("%H", time.localtime(self._time)))
        return hour


    # get the minute for the alarm
    def getMinute(self):
        minute = int(time.strftime("%M", time.localtime(self._time)))
        return minute


    # activate the alarm
    def activate(self):
        self._activated = True


    # deactivate the alarm
    def deactivate(self):
        self._activated = False


    # toggle activated/deactivated
    def toggleActivated(self):
        if self._activated:
            self._activated = False

        else: self._activated = True


    # return string for saving in textfile
    def savingStr(self):
        return str(self._time)+';'+str(self._fromCalendar)+';'+str(self._activated)


    # return a string describing the alarm
    def printingStr(self):
        active = ' Inactive'
        if self._activated:
            active = ' Active'
        fromCal = ''
        if self._fromCalendar:
            fromCal = ' from calendar'
        return str(str(self)+active+fromCal)
