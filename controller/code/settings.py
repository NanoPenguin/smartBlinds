"""
Class for loading the settings from
web interface or local drive
"""

class Settings():
    alarmTimes[]
    activeManualAlarms[]

    def __init__(self,path="",loadFromWeb=False):
        if loadFromWeb:
            loadWebData()
        else:
            loadLocalData()

    def loadWebData():
        #Funktion som läser in alla
        #inställningar från webinterface
        manualAlarmTimes.append("12")


    def loadLocalData():
        #Funktion som läser in alla
        #inställningar från en lokal textfil
        manualAlarmTimes.append("something else")
