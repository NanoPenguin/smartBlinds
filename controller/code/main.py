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

# must be initialized settings - alarms - screen
SETTINGS = Settings()  # initializing settings
ALARMS = SETTINGS.getSetting('Alarms')  # initializing alarms
SCREEN = Screen(ALARMS, SETTINGS)  # initializing screen


def main():
    newAlarm(time.time())
    newAlarm(time.time(), True, False)
    newAlarm(time.time(), False, True)
    newAlarm(time.time(), True, True)
    newAlarm(time.time(), True, False)

    SCREEN.messageScreen("""This is a
    message""")

    SCREEN.alarmScreen()
    time.sleep(1)
    SCREEN.scrollDown()
    time.sleep(2)
    SCREEN.scrollDown()
    time.sleep(0.2)
    SCREEN.scrollDown()
    SCREEN.scrollDown()
    SCREEN.scrollUp()
    print(SCREEN.selectedAlarm())
    removeAlarm(SCREEN.selectedAlarm())
    SCREEN.resetScroll()
    SCREEN.alarmScreen()
    time.sleep(0.3)
    SCREEN.scrollDown()
    time.sleep(1)

    SCREEN.settingsScreen()
    time.sleep(0.2)
    SCREEN.scrollDown()
    time.sleep(0.2)
    SCREEN.scrollUp()
    time.sleep(0.2)
    SCREEN.scrollDown()
    time.sleep(0.2)
    print(SCREEN.selectedSetting())
    time.sleep(2)

    SCREEN.clockScreen()
    time.sleep(2)
    SCREEN.setHourScreen(str(ALARMS[0]))
    time.sleep(2)
    SCREEN.setMinuteScreen(str(ALARMS[0]))
    time.sleep(2)

    SETTINGS.saveSettings()


# alarms=alarmArray, time=any time in seconds since epoch
def newAlarm(time, fromCalendar=False, activated=True):
    newAlarm = Alarm(time, fromCalendar, activated)
    ALARMS.append(newAlarm)


def removeAlarm(alarm):
    ALARMS.remove(alarm)


main()
