"""
main code for control unit
runs on raspberry pi zero w
"""

from alarm import *
from settings import *
from blinds import *
from comm import *
from screen import *

"""
timeTuple = (2020,11,11,12,12,13,2,67,-1)
year, mon, day, h, m, s, wd, yd, -1
epochSeconds = time.mktime(timeTuple)
"""

def main():
    alarms = [] # Array of alarm objects


# reads from file and regreates saved alarms, settings and blids
# has to creat global objects
def readFromFile():
    pass


# writs alarms, settings and blids to file
def writeToFile():
    pass


# called from alarmScreen()
# alarms=alarmArray, time=any time in seconds since epoch
def newAlarm(alarms, time):
    newAlarm = Alarm(time)
    alarms.append(newAlarm)


main()
