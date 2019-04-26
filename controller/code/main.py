"""
main code for control unit
runs on raspberry pi zero w
"""

import time

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
    alarms = []  # Array of alarm objects
    screen = Screen(alarms)  # initialising screen
    newAlarm(alarms, time.time())
    newAlarm(alarms, time.time(), True, False)
    newAlarm(alarms, time.time(), False, True)
    newAlarm(alarms, time.time(), True, True)
    newAlarm(alarms, time.time(), True, False)
    screen.alarmScreen()
    time.sleep(0.4)
    screen.alarmScrollDown()
    time.sleep(0.4)
    screen.alarmScrollDown()
    time.sleep(0.4)
    screen.alarmScrollDown()
    screen.alarmScrollDown()
    time.sleep(0.4)
    screen.alarmScrollUp()
    time.sleep(0.4)
    screen.alarmScrollUp()
    time.sleep(0.4)
    screen.alarmScrollUp()
    time.sleep(0.4)
    screen.alarmScrollDown()
    time.sleep(0.4)
    print(screen.selectedAlarm())
    screen.clockScreen()
    time.sleep(3)


# reads from file and regreates saved alarms, settings and blids
# has to creat global objects
def readFromFile():
    pass


# writs alarms, settings and blids to file
def writeToFile():
    pass


# called from alarmScreen()
# alarms=alarmArray, time=any time in seconds since epoch
def newAlarm(alarms, time, fromCalendar=False, activated=True):
    newAlarm = Alarm(time, fromCalendar, activated)
    alarms.append(newAlarm)


main()
