"""
Dummy-class for NO contact with google calendar
"""

class Cal():
    def __init__(self,calendarId=None):
        pass

    def loadCalendarIds(self):
        pass

    def setDayTomorrow(self):
        pass

    def getFirstEvent(self, calendarId):
        return None

    def initCreds(self):
        return True

    def getCalendarAlarms(self,calMargin):
        calendarAlarms = []
        return calendarAlarms
