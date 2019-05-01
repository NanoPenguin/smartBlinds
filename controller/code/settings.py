"""
Class for loading the settings from
web interface or local drive
"""

class Settings():
    self._settings = {
    'alarms': [],
    'preEventDelay': ''
    }

    def __init__(self, path="", loadFromWeb=False):
        if loadFromWeb:
            loadWebData()
        else:
            loadLocalData()
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
