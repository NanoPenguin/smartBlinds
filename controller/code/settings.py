"""
Class for loading the settings from
web interface or local drive
"""

from collections import OrderedDict

from alarm import *

class Settings():
    def __init__(self, path="", loadFromWeb=False):
        self._settings = OrderedDict()
        self._settings['alarms'] = [],
        self._settings['preEventDelay'] = ''
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
        pass


    def _createAlarms(self):
        alarms = []
        for alarm in self._settings['alarms']:
            alarms.append(Alarm(alarm['time'], alarm['fromCalendar'], alarm['isActivated']))
        self._settings['alarms'] = alarms


    def getKeys(self):
        keys = [key for key in self._settings.items()]
        return keys
