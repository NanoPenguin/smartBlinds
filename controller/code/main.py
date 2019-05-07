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


# Global messageDelay
MESSAGEDELAY = 1


def main():
    # Load alarmtimes from calendar
    # ALARMS.append(CAL.getCalendarAlarms())

    while True:
        input = IO.waitForInput()
        if input is 'up':
            SOUND.increaseFreq()
            SCREEN.messageScreen(['UP'+str(SOUND.getFreq())])
        elif input is 'down':
            SOUND.decreaseFreq()
            SCREEN.messageScreen(['DOWN'+str(SOUND.getFreq())])
        elif input is 'left':
            SOUND.stopSound()
            SCREEN.messageScreen(['LEFT'+str(SOUND.getFreq())])
        elif input is 'right':
            SOUND.makeSound()
            SCREEN.messageScreen(['RIGHT'+str(SOUND.getFreq())])
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


def clockScreen():
    while True:
        SCREEN.clockScreen()
        input = IO.readInput()
        if input:
            if input is 'left':
                pass
            elif input is 'up':
                newAlarmScreen()
            elif input is 'down':
                pass
            elif input is 'right':
                settingsScreen()
        time.sleep(0.1)


def newAlarmScreen():
    message(['Set new Alarm'])
    newAlarm = newAlarm(time.localtime(time.time()))
    while True:
        SCREEN.setHourScreen(str(newAlarm))
        input = IO.waitForInput()
        if input is 'left':
            message(['Alarm discarded'])
            return False
        elif input is 'up':
            newAlarm.setTime(newAlarm.getTime()+3600)
        elif input is 'down':
            newAlarm.setTime(newAlarm.getTime()-3600)
        elif input is 'right':
            while True:
                SCREEN.setMinuteScreen(str(newAlarm))
                input = IO.waitForInput()
                if input is 'left':
                    break
                elif input is 'up':
                    newAlarm.setTime(newAlarm.getTime()+60)
                elif input is 'down':
                    newAlarm.setTime(newAlarm.getTime()-60)
                elif input is 'right':
                    ALARMS.append(newAlarm)
                    message(['Alarm set'])
                    return True


def settingsScreen():
    message(['Settings'])
    SCREEN.settingsScreen()
    while True:
        input = IO.waitForInput()
        if input is 'left':
            return False
        elif input is 'up':
            SCREEN.scrollUp()
        elif input is 'down':
            screen.scrollDown()
        elif input is 'right':
            setting = SCREEN.selectedSetting()
            if setting is 'Alarms':
                alarmListScreen()
            elif setting in ['Close direction']:
                value = SETTINGS.getSetting(setting)
                if value:
                    value = 0
                else:
                    value = 1
                SETTINGS.setSetting(setting, value)
                if setting is 'Close direction':
                    if value:
                        direction = 'up'
                    else:
                        direction = 'down'
                    message(['Close direction', 'set to '+direction])
                if setting is 'Cal. margin':
                    message(['Set time for' ,'wake-up before', 'first event'])
                    previous = SETTINGS.getSetting('Cal. margin')
                    hours = int(previous/3600)
                    minutes = int((previous%3600)/60)
                    while True:
                        SCREEN.setHourScreen(toTimeStr(hours, minutes))
                        input = IO.waitForInput()
                        if input is 'left':
                            message(['Changes discarded'])
                            break
                        elif input is 'up':
                            hours+=1
                        elif input is 'down':
                            hours-=1
                        elif input is 'right':
                            while True:
                                SCREEN.setMinuteScreen(toTimeStr(hours, minutes))
                                input = IO.waitForInput()
                                if input is 'left':
                                    break
                                elif input is 'up':
                                    minutes+=1
                                elif input is 'down':
                                    minutes-=1
                                elif input is 'right':
                                    message(['Value changed'])
                                    break
                            if 


def alarmListScreen():
    pass


def displayMessage(message):
    SCREEN.displayMessage(message)
    time.sleep(MESSAGEDELAY)


def toTimeStr(hours, minutes):
    if hours < 10:
        hourStr = '0'+str(hours)
    else:
        hourStr = str(hours)
    if minutes < 10:
        minuteStr = '0'+str(minutes)
    else:
        minuteStr = str(minutes)
    return hourStr+':'+minuteStr


main()
