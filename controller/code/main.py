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

SETTINGS = Settings()  # initializing settings
ALARMS = SETTINGS.getSetting('Alarms')  # initializing alarms
SCREEN = Screen(ALARMS, SETTINGS)  # initializing screen
BLINDS =  Blinds() # initializing blinds
CAL = Cal()  # initializing calendar
IO = Io()  # Initializing GPIO
SOUND = Sound() # Initializing Sound

# global timeconstants
MESSAGEDELAY = 0.7
BUTTONHOLDDELAY = 1
INPUTTIMEOUT = 10
CAL_CHANGE_DAY_TIME = '17:00'

# global calendar related variables
LASTTRIGGEREDMINUTE = 100
CAL_UPDATED = False
CAL_DAY_CHANGED = False


# main function
def main():
    updateCalAlarms()
    clockScreen()


# create and append new alarm
def newAlarm(time, fromCalendar=False, activated=True):
    newAlarm = Alarm(time, fromCalendar, activated)
    ALARMS.append(newAlarm)


# remove alarm from list
def removeAlarm(alarm):
    ALARMS.remove(alarm)


# enter the clockscreen-loop
def clockScreen():
    while True:
        watchAlarms()
        SCREEN.clockScreen()
        waitForRelease()
        input = IO.waitForInput(1)
        if input is 'left':
            newAlarmScreen()
            SETTINGS.saveSettings()
        elif input is 'up':
            #connected = BLINDS.open()
            BLINDS.setAngle(600,SETTINGS.getSetting('Easy wake')*1000)
            if not connected:
                message(['Blinds not', 'connected'])
        elif input is 'down':
            if SETTINGS.getSetting('Close dir'):
                connected = BLINDS.up()
            else:
                connected = BLINDS.down()
            if not connected:
                message(['Blinds not', 'connected'])
        elif input is 'right':
            settingsScreen()
            SETTINGS.saveSettings()


# enter newalarm-loop
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


# enter settings-loop
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
                    elif input is 'right' or setting is 'Easy wake':
                        toBreak = False
                        while True:
                            watchAlarms()
                            SCREEN.setMinuteScreen(toTimeStr(hours, minutes))
                            waitForRelease()
                            input = IO.waitForInput()
                            if input is 'left':
                                if setting is 'Easy wake':
                                    toBreak = True
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
            elif setting is 'exit':
                quit()


# enter alarmlist-loop
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
            if SCREEN.selectedAlarm() == 'newAlarm':
                newAlarmScreen()
            elif SCREEN.selectedAlarm() == 'updateCalAlarms':
                message(['Updating','cal alarms'])
                updateCalAlarms()
                SCREEN.resetScroll()
            elif SCREEN.selectedAlarm() == 'nextDay':
                message(['Changing','calendar day'])
                CAL.setDayTomorrow()
                updateCalAlarms()
                SCREEN.resetScroll()
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


# display a message in 1-3 rows
def message(message):
    watchAlarms()
    SCREEN.messageScreen(message)
    time.sleep(MESSAGEDELAY)


# convert integers to a 24h-clock string in the format HH:MM
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


# convert a string of format HH:MM into integers
def toTimeInt(timeStr):
    hour, minute = timeStr.split(':')
    hour = int(hour)
    minute = int(minute)
    return hour, minute


# wait for release of button or until timeout
def waitForRelease():
    now = time.time()
    while IO.readInput():
        time.sleep(0.1)
        then = time.time()
        if then-now>INPUTTIMEOUT:
            return False


# trigger alarms, open blinds and update calendar events
def watchAlarms():
    global CAL_UPDATED
    global LASTTRIGGEREDMINUTE
    now = time.strftime("%H:%M", time.localtime(time.time()))
    nowHour, nowMinute = toTimeInt(now)
    if not nowMinute and not CAL_UPDATED:
        if now == CAL_CHANGE_DAY_TIME and not CAL_DAY_CHANGED:
            CAL.setDayTomorrow()
            CAL_DAY_CHANGED = True
        updateCalAlarms()
        CAL_UPDATED = True
    elif nowMinute:
        CAL_UPDATED = False
    elif int(now[0:2]) > int(CAL_CHANGE_DAY_TIME[0:2])+1:
        CAL_DAY_CHANGED = False
    if nowMinute!=LASTTRIGGEREDMINUTE and LASTTRIGGEREDMINUTE != 100:
        LASTTRIGGEREDMINUTE = 100
    else:
        for alarm in ALARMS:
            if alarm.isActivated():
                hour = alarm.getHour()
                minute = alarm.getMinute()
                alarmTime = alarm.getTime()
                blindTime = time.strftime("%H:%M", time.localtime(alarmTime-SETTINGS.getSetting('Easy wake')))
                blindHour, blindMinute = toTimeInt(blindTime)
                if nowHour==hour and nowMinute==minute:
                    alarm.toggleActivated()
                    LASTTRIGGEREDMINUTE = minute
                    triggerAlarm()
                elif blindHour==hour and blindMinute==minute:
                    LASTTRIGGEREDMINUTE = minute
                    BLINDS.setAngle(600,SETTINGS.getSetting('Easy wake')*1000)


# update calendar alarms
def updateCalAlarms():
    newCalAlarms = CAL.getCalendarAlarms(SETTINGS.getSetting('Cal. margin'))
    if newCalAlarms != 'ERROR':
        removed = True
        while removed:
            removed = False
            for alarm in ALARMS:
                if alarm.isFromCalendar():
                    removeAlarm(alarm)
                    removed = True

        for alarm in newCalAlarms:
            ALARMS.append(alarm)


# trigger alarm and beep until turned of
def triggerAlarm():
    print('ALARM TRIGGERED')
    while True:
        input = IO.readInput()
        if input is 'up':
            message(['Alarm stopped'])
            SOUND.stop()
            break
        SOUND.beep(0.5)
        SCREEN.clockScreen()


main()
