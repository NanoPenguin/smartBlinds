"""
Class for loading the settings from local settings.txt file
"""

from collections import OrderedDict

from alarm import *


class Settings():
    def __init__(self):
        self._file = 'settings.txt'
        self._settings = OrderedDict()
        self._settings['Alarms'] = []
        self._settings['Cal. margin'] = 0
        self._settings['Easy wake'] = 100
        self._settings['Close dir'] = 1 # 1 or 0, 1=up 0=down
        self.loadLocalData()
        self._createAlarms()


    # get a specific setting
    def getSetting(self, key):
        return self._settings[key]


    # set a specific setting
    def setSetting(self, key, value):
        self._settings[key] = value


    # get the entire settings dictionary
    def getAll(self):
        return self._settings


    # load settings stored to settings.txt
    def loadLocalData(self):
        print('Reading settings from file:')
        try:
            file = open(self._file, 'r')
            for line in file.readlines():
                line = line.strip('\n')
                splitline = line.split(':')
                key = splitline[0]
                if key == 'Alarms':
                    alarms = splitline[1].split('/')
                    splittedAlarms = []
                    for alarm in alarms:
                        alarm = alarm.split(';')
                        splittedAlarms.append(alarm)
                    if splittedAlarms[0][0]:
                        value = [{'time': float(alarm[0]), 'fromCalendar': alarm[1], 'isActivated': alarm[2]} for alarm in splittedAlarms]
                    else:
                        value = []
                    for alarm in value:
                        if alarm['fromCalendar'] == 'True':
                            alarm['fromCalendar'] = True
                        else: alarm['fromCalendar'] = False
                        if alarm['isActivated'] == 'True':
                            alarm['isActivated'] = True
                        else: alarm['isActivated'] = False
                if key in ['Cal. margin', 'Easy wake', 'Close dir']:
                    value = int(splitline[1])
                print('\t'+key+': '+str(value))
                self._settings[key] = value
            file.close()
        except FileNotFoundError:
            print('No settings.txt found')


    # save all settings to settings.txt
    def saveSettings(self):
        print('Saving the following settings:')
        file = open(self._file, 'w')
        for key, value in self._settings.items():
            if key == 'Alarms':
                alarms = []
                for alarm in value:
                    alarms.append(alarm.savingStr())
                value = ('/').join(alarms)
            elif key in ['Cal. margin', 'Easy wake', 'Close dir']:
                value = str(value)
            else:
                continue
            print('\t'+key+': '+value)
            file.write(key+':'+value+'\n')
        file.close()


    # create alarm objects of the data found in settings.txt
    def _createAlarms(self):
        alarms = []
        alarmList = self._settings['Alarms']
        for alarm in alarmList:
            alarms.append(Alarm(alarm['time'], alarm['fromCalendar'], alarm['isActivated']))
        self._settings['Alarms'] = alarms


    # get all the keys for the settings dictionary
    def getKeys(self):
        keys = [key[0] for key in self._settings.items()]
        return keys


    # add an alarm to settings
    def addAlarm(self, alarm):
        self._settings['Alarms'].append(alarm)
