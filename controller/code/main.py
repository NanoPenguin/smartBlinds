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
    alarms = settings.getSetting('Alarms')  # initializing alarms
    screen = Screen(alarms, settings)  # initializing screen

    newAlarm(time.time())
    newAlarm(time.time(), True, False)
    newAlarm(time.time(), False, True)
    newAlarm(time.time(), True, True)
    newAlarm(time.time(), True, False)

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
    removeAlarm(screen.selectedAlarm())
    screen.resetScroll()
    screen.alarmScreen()
    time.sleep(0.3)
    screen.scrollDown()
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
    time.sleep(2)

    settings.saveSettings()


    # alarms=alarmArray, time=any time in seconds since epoch
    def newAlarm(time, fromCalendar=False, activated=True):
        newAlarm = Alarm(time, fromCalendar, activated)
        alarms.append(newAlarm)


    def removeAlarm(alarm):
        alarms.remove(alarm)


main()
