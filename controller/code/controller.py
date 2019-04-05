"""
main code for control unit
runs on raspberry pi zero w
"""
from alarm import *
from settings import *
from blinds import *
from comm import *
from screen import *

def main():
    alarms =[] # Array of alarm objects
    pass

# reads from file and regreates saved alarms, settings and blids
# has to creat global objects
def readFromFile():
    pass

# writs alarms, settings and blids to file
def writeToFile():
    pass

# called from alarmScreen()
def creatAlarm(time):
    alarms[len(alarms)] = alarm(time)


main()
