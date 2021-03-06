"""
Class for contact with google calendar
"""

from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
import httplib2
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tz import LocalTimezone

from alarm import *

#Delete file token.pickle when modifying scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class Cal():
    def __init__(self,calendarId=None):
        self._calendarIdList = []
        self.initCreds()
        if calendarId:
            self._calendarIdList.append(calendarId)
        currentTime = datetime.datetime.utcnow()
        if currentTime.hour>=13:
            self.setDayTomorrow()
        else:
            self._alarmDate = currentTime.replace(day=currentTime.day,hour=0,minute=0,second=0)


    # load personal calendarIds from google account
    def loadCalendarIds(self):
        ignoreIdList = ['e_2_sv#weeknum@group.v.calendar.google.com',
                'sv.swedish#holiday@group.v.calendar.google.com',
                'addressbook#contacts@group.v.calendar.google.com']
        calendarList = self._service.calendarList().list().execute()
        for calendar in calendarList['items']:
            id = calendar['id']
            if id not in ignoreIdList:
                self._calendarIdList.append(id)


    # set alarmday to next day
    def setDayTomorrow(self):
        currentTime = datetime.datetime.utcnow()
        self._alarmDate = currentTime.replace(day=currentTime.day+1,hour=0,minute=0,second=0)


    # Get the first event (after 00:00) for calendar with given id.
    # Returns a time object or None if no event is found
    def getFirstEvent(self, calendarId):
        print('Getting upcoming morning event for '+calendarId)
        currentTime = datetime.datetime.utcnow()
        # Start and stop date for next day
        start = self._alarmDate
        stop = self._alarmDate.replace(day=self._alarmDate.day+1)
        startDate = start.isoformat()+'Z'
        stopDate = stop.isoformat()+'Z'
        try:
            eventsResult = self._service.events().list(calendarId=calendarId, timeMin=startDate,
                                                timeMax=stopDate,maxResults=100, singleEvents=True,
                                                orderBy='startTime').execute()
            events = eventsResult.get('items', [])
        except httplib2.ServerNotFoundError:
            events = None

        if events:
            for event in events:
                eventStart = event['start'].get('dateTime', event['start'].get('date'))
                startTime = dateutil.parser.parse(eventStart)
                try:
                    startTime = startTime.astimezone(LocalTimezone())
                except ValueError:
                    print('Catched ValueError')
                startTimeStr = startTime.strftime('%H:%M')
                if startTimeStr != '00:00':
                    print(startTimeStr, event['summary'])
                    return time.mktime(startTime.timetuple())
        return None


    # init credentials and connect to google account
    def initCreds(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server()
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self._credsInitialized = False
        try:
            service = build('calendar', 'v3', credentials=creds)
            self._credsInitialized = True
        except httplib2.ServerNotFoundError:
            print('No connection to server')
            return False
        self._service = service
        self.loadCalendarIds()
        return True


    # Returns list with Alarm-objects based on the first event
    # from each personal calendar.
    # The earliest alarm in the list is activated.
    def getCalendarAlarms(self,calMargin):
        if not self._credsInitialized:
            if not self.initCreds():
                return 'ERROR'

        calendarAlarms = []
        earliest = None
        earliestIndex = -1
        i=0
        for calendarId in self._calendarIdList:
            startTime = self.getFirstEvent(calendarId)
            if startTime:
                startTime -= calMargin
                if (not earliest) or startTime<earliest:
                    earliest = startTime
                    earliestIndex = i
                calendarAlarms.append(Alarm(startTime,True,False))
                i+=1
        if earliestIndex != -1:
            try:
                calendarAlarms[earliestIndex].activate()
            except IndexError:
                pass
        return calendarAlarms
