"""
main code for control unit
runs on raspberry pi zero w
"""

import time

from alarm import *
from settings import *
from blinds import *
from communication import *
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
BLINDS =  Blinds() # initializing blinds
CAL = Cal()  # initializing calendar
IO = Io()  # Initializing GPIO
SOUND = Sound() # Initializing Sound


# Global timeconstants
MESSAGEDELAY = 0.7
BUTTONHOLDDELAY = 1
INPUTTIMEOUT = 10

LASTTRIGGEREDMINUTE = 100


def main():
    # Load alarmtimes from calendar
    # ALARMS.append(CAL.getCalendarAlarms())

    clockScreen()


# alarms=alarmArray, time=any time in seconds since epoch
def newAlarm(time, fromCalendar=False, activated=True):
    newAlarm = Alarm(time, fromCalendar, activated)
    ALARMS.append(newAlarm)


def removeAlarm(alarm):
    ALARMS.remove(alarm)


def clockScreen():
    while True:
        watchAlarms()
        SCREEN.clockScreen()
        waitForRelease()
        input = IO.waitForInput()
        if input:
            if input is 'left':
                newAlarmScreen()
                SETTINGS.saveSettings()
            elif input is 'up':
                connected = BLINDS.up()
                if not connected:
                    message(['Blinds not', 'connected'])
            elif input is 'down':
                connected = BLINDS.down()
                if not connected:
                    message(['Blinds not', 'connected'])
            elif input is 'right':
                settingsScreen()
                SETTINGS.saveSettings()


def newAlarmScreen():
    message(['Set new', 'alarm'])
    newAlarm = Alarm(time.time())
    while True:
        watchAlarms()
        SCREEN.setHourScreen(str(newAlarm))
        waitForRelease()
        input = IO.waitForInput()
        if input is 'left':
            message(['Alarm', 'discarded'])
            return False
        elif input is 'up':
            newAlarm.setTime(newAlarm.getTime()+3600)
        elif input is 'down':
            newAlarm.setTime(newAlarm.getTime()-3600)
        elif input is 'right':
            while True:
                watchAlarms()
                SCREEN.setMinuteScreen(str(newAlarm))
                waitForRelease()
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
    while True:
        watchAlarms()
        SCREEN.settingsScreen()
        waitForRelease()
        input = IO.waitForInput()
        if input is 'left':
            return False
        elif input is 'up':
            SCREEN.scrollUp()
        elif input is 'down':
            SCREEN.scrollDown()
        elif input is 'right':
            setting = SCREEN.selectedSetting()
            if setting is 'Alarms':
                alarmListScreen()
            elif setting in ['Close dir']:
                value = SETTINGS.getSetting(setting)
                if value:
                    value = 0
                else:
                    value = 1
                SETTINGS.setSetting(setting, value)
                if value:
                    direction = 'up'
                else:
                    direction = 'down'
                message(['Close dir', 'set to '+direction])
            elif setting in ['Cal. margin', 'Easy wake']:
                if setting == 'Cal. margin':
                    mes = ['Set time for' ,'wake-up before', 'first event']
                elif setting == 'Easy wake':
                    mes = ['Set how long', 'it takes to', 'open blinds']
                message(mes)
                time.sleep(MESSAGEDELAY)
                previous = SETTINGS.getSetting(setting)
                hours = int(previous/3600)
                minutes = int((previous%3600)/60)
                while True:
                    watchAlarms()
                    SCREEN.setHourScreen(toTimeStr(hours, minutes))
                    waitForRelease()
                    input = IO.waitForInput()
                    if input is 'left':
                        message(['Changes', 'discarded'])
                        break
                    elif input is 'up':
                        hours+=1
                        if hours == 24:
                            hours = 0
                    elif input is 'down':
                        hours-=1
                        if hours < 0:
                            hours = 23
                    elif input is 'right':
                        toBreak = False
                        while True:
                            watchAlarms()
                            SCREEN.setMinuteScreen(toTimeStr(hours, minutes))
                            waitForRelease()
                            input = IO.waitForInput()
                            if input is 'left':
                                break
                            elif input is 'up':
                                minutes+=1
                                if minutes == 60:
                                    minutes = 0
                            elif input is 'down':
                                minutes-=1
                                if minutes < 0:
                                    minutes = 59
                            elif input is 'right':
                                SETTINGS.setSetting(setting, hours*3600+minutes*60)
                                message(['Value', 'changed'])
                                toBreak = True
                                break
                        if toBreak:
                            break


def alarmListScreen():
    while True:
        watchAlarms()
        SCREEN.alarmScreen()
        waitForRelease()
        input = IO.waitForInput()
        if input is 'left':
            break
        elif input is 'up':
            SCREEN.scrollUp()
        elif input is 'down':
            SCREEN.scrollDown()
        elif input is 'right':
            if not SCREEN.selectedAlarm():
                newAlarmScreen()
            else:
                now = time.time()
                while True:
                    if not IO.readInput() or time.time()-now > BUTTONHOLDDELAY:
                        break
                then = time.time()
                alarm = SCREEN.selectedAlarm()
                if then-now < BUTTONHOLDDELAY:
                    alarm.toggleActivated()
                else:
                    SCREEN.messageScreen(['Delete?', 'NO       YES'])
                    waitForRelease()
                    input = IO.waitForInput()
                    if input is 'left':
                        message(['Not deleted'])
                    elif input is 'right':
                        removeAlarm(alarm)
                        message(['Deleted'])



def message(message):
    watchAlarms()
    SCREEN.messageScreen(message)
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


def toTimeInt(timeStr):
    hour, minute = timeStr.split(':')
    hour = int(hour)
    minute = int(minute)
    return hour, minute


def waitForRelease():
    now = time.time()
    while IO.readInput():
        time.sleep(0.1)
        then = time.time()
        if then-now>INPUTTIMEOUT:
            return False


def watchAlarms():
    global LASTTRIGGEREDMINUTE
    if nowMinute!=LASTTRIGGEREDMINUTE:
        LASTTRIGGEREDMINUTE = 100
    else:
        activeAlarms = []
        for alarm in ALARMS:
            if alarm.isActivated():
                activeAlarms.append(alarm)
        now = time.strftime("%H:%M", time.localtime(time.time()))
        nowHour, nowMinute = toTimeInt(now)
        for alarm in activeAlarms:
            hour = alarm.getHour()
            minute = alarm.getMinute()
            if nowHour==hour and nowMinute==minute:
                if alarm.isFromCalendar():
                    removeAlarm(alarm)
                else:
                    alarm.toggleActivated()
                LASTTRIGGEREDMINUTE = minute
                triggerAlarm()


def triggerAlarm():
    print('ALARM TRIGGERED')


main()
