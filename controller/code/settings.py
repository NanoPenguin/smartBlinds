"""
Class for loading the settings from
web interface or local drive
"""

from collections import OrderedDict

from alarm import *

class Settings():
    def __init__(self, loadFromWeb=False):
        self._file = 'settings.txt'
        self._settings = OrderedDict()
        self._settings['Alarms'] = []
        self._settings['Cal. margin'] = 0
        self._settings['Easy wake'] = 0
        if loadFromWeb:
            self.loadWebData()
        else:
            self.loadLocalData()
        self._createAlarms()


    def getSetting(self, key):
        return self._settings[key]


    def getAll(self):
        return self._settings


    def loadWebData(self):
        #Funktion som läser in alla
        #inställningar från webinterface
        pass


    def loadLocalData(self):
        #Funktion som läser in alla
        #inställningar från en lokal textfil
        print('Reading settings from file:')
        try:
            file = open(self._file, 'r')
            for line in file.readlines():
                splitline = line.split(':')
                key = splitline[0]
                if key == 'Alarms':
                    alarms = splitline[1].split('/')
                    for alarm in alarms:
                        alarm = alarm.split(',')
                    value = [{'time': int(alarm[0]), 'fromCalendar': alarm[1], 'isActivated': alarm[2]} for alarm in alarms]
                    for alarm in value:
                        if alarm['fromCalendar'] == 'True':
                            alarm['fromCalendar'] = True
                        else: alarm['fromCalendar'] = False
                        if alarm['isActivated'] == 'True':
                            alarm['isActivated'] = True
                        else: alarm['isActivated'] = False
                if key in ['Cal. margin', 'Easy wake']:
                    value = int(splitline[1])
                print('\t'+key+': '+str(value))
                self._settings[key] = value
            file.close()
        except FileNotFoundError:
            print('No settings.txt found')


    def saveSettings(self):
        print('Saving the following settings:')
        file = open(self._file, 'w')
        for key, value in self._settings.items():
            if key == 'Alarms':
                alarms = []
                for alarm in value:
                    alarms.append(alarm.savingStr())
                value = ('/').join(alarms)
            elif key in ['Cal. margin', 'Easy wake']:
                value = str(value)
            print('\t'+key+': '+value)
            file.write(key+':'+value+'\n')
        file.close()


    def _createAlarms(self):
        alarms = []
        alarmList = self._settings['Alarms']
        for alarm in alarmList:
            alarms.append(Alarm(alarm['time'], alarm['fromCalendar'], alarm['isActivated']))
        self._settings['Alarms'] = alarms


    def getKeys(self):
        keys = [key[0] for key in self._settings.items()]
        return keys


    def addAlarm(self, alarm):
        self._settings['Alarms'].append(alarm)
