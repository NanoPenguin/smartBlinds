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
    # must be initialized settings - alarms - screen
    settings = Settings()  # initializing settings
    alarms = settings.getSetting('alarms')  # initializing alarms
    screen = Screen(alarms, settings)  # initializing screen

    newAlarm(alarms, time.time())
    newAlarm(alarms, time.time(), True, False)
    newAlarm(alarms, time.time(), False, True)
    newAlarm(alarms, time.time(), True, True)
    newAlarm(alarms, time.time(), True, False)

    screen.settingsScreen()
    time.sleep(0.2)
    screen.scrollDown()
    time.sleep(0.2)
    screen.scrollUp()
    time.sleep(0.2)
    screen.scrollDown()
    time.sleep(0.2)
    print(screen.selectedSetting())
    time.sleep(2)

    screen.alarmScreen()
    time.sleep(1)
    screen.scrollDown()
    time.sleep(2)
    screen.scrollDown()
    time.sleep(0.2)
    screen.scrollDown()
    screen.scrollDown()
    screen.scrollUp()
    print(screen.selectedAlarm())
    time.sleep(1)

    screen.settingsScreen()
    time.sleep(0.2)
    screen.scrollDown()
    time.sleep(0.2)
    screen.scrollUp()
    time.sleep(0.2)
    screen.scrollDown()
    time.sleep(0.2)
    print(screen.selectedSetting())
    time.sleep(2)

    screen.clockScreen()
    time.sleep(2)
    screen.setHourScreen(str(alarms[0]))
    time.sleep(2)
    screen.setMinuteScreen(str(alarms[0]))
    time.sleep(5)


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
