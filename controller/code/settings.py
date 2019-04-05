"""
Class for loading the settings from
web interface or local drive
"""

class Settings():
    manualAlarmTimes[]
    manualAlarmsActive[]

    def __init__(self,path="",loadFromWeb=False):
        if loadFromWeb:
            loadWedData()
        else:
            loadLocalData()

    def loadWebData():
        #Funktion som läser in alla
        #inställningar från webinterface
        manualAlarmTimes.append("something")


    def loadLocalData():
        #Funktion som läser in alla
        #inställningar från en lokal textfil
        manualAlarmTimes.append("something else")
