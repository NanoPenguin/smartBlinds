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
from cal import *
from gpio import *
from sound import *

"""
timeTuple = (2020,11,11,12,12,13,2,67,-1)
year, mon, day, h, m, s, wd, yd, -1
epochSeconds = time.mktime(timeTuple)
"""

# must be initialized settings - alarms - screen in that exact order
SETTINGS = Settings()  # initializing settings
ALARMS = SETTINGS.getSetting('Alarms')  # initializing alarms
SCREEN = Screen(ALARMS, SETTINGS)  # initializing screen
BLINDS = Blinds(SETTINGS.getSetting('Blinds angle'))  # initializing blinds
CAL = Cal()  # initializing calendar
IO = Io()  # Initializing GPIO
SOUND = Sound() # Initializing Sound


def main():
    # Load alarmtimes from calendar
    # ALARMS.append(CAL.getCalendarAlarms())

    while True:
        input = IO.waitForInput()
        if input is 'up':
            SCREEN.messageScreen(['UP'])
            SOUND.makeSound()
        elif input is 'down':
            SCREEN.messageScreen(['DOWN'])
        elif input is 'left':
            SCREEN.messageScreen(['LEFT'])
        elif input is 'right':
            SCREEN.messageScreen(['RIGHT'])
        time.sleep(0.3)

    SCREEN.messageScreen(['This message'])
    time.sleep(1)
    SCREEN.messageScreen(['This is a', 'message'])
    time.sleep(1)
    SCREEN.messageScreen(['This is', 'another', 'message'])
    time.sleep(1)

    SCREEN.alarmScreen()
    time.sleep(0.5)
    SCREEN.scrollDown()
    time.sleep(0.5)
    SCREEN.scrollDown()
    time.sleep(0.2)
    SCREEN.scrollDown()
    SCREEN.scrollDown()
    SCREEN.scrollUp()
    print(SCREEN.selectedAlarm())
    removeAlarm(SCREEN.selectedAlarm())
    SCREEN.messageScreen(['Alarm removed'])
    time.sleep(1)
    SCREEN.alarmScreen()
    time.sleep(1)
    SCREEN.scrollDown()
    time.sleep(0.5)

    SCREEN.settingsScreen()
    time.sleep(0.2)
    SCREEN.scrollDown()
    time.sleep(0.2)
    SCREEN.scrollUp()
    time.sleep(0.2)
    SCREEN.scrollDown()
    time.sleep(0.2)
    print(SCREEN.selectedSetting())
    time.sleep(1)

    SCREEN.clockScreen()
    time.sleep(1)
    SCREEN.setHourScreen(str(ALARMS[0]))
    time.sleep(1)
    SCREEN.setMinuteScreen(str(ALARMS[0]))
    time.sleep(1)

    SETTINGS.saveSettings()


# alarms=alarmArray, time=any time in seconds since epoch
def newAlarm(time, fromCalendar=False, activated=True):
    newAlarm = Alarm(time, fromCalendar, activated)
    ALARMS.append(newAlarm)


def removeAlarm(alarm):
    ALARMS.remove(alarm)


main()
