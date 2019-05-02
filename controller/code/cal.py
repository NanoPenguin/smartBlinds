from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
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
        self.loadCalendarIds()



    def loadCalendarIds(self):
        ignoreIdList = ['e_2_sv#weeknum@group.v.calendar.google.com',
                'sv.swedish#holiday@group.v.calendar.google.com',
                'addressbook#contacts@group.v.calendar.google.com']
        calendarList = self._service.calendarList().list().execute()
        for calendar in calendarList['items']:
            id = calendar['id']
            if id not in ignoreIdList:
                self._calendarIdList.append(id)

    def getFirstEvent(self,calendarId):
        print('Getting upcoming morning event for '+calendarId)
        currentTime = datetime.datetime.utcnow()
        # Start and stop date for next day
        start = currentTime.replace(day=currentTime.day+1,hour=0,minute=0,second=0)
        stop = currentTime.replace(day=currentTime.day+2,hour=0,minute=0,second=0)
        startDate = start.isoformat()+'Z'
        stopDate = stop.isoformat()+'Z'
        eventsResult = self._service.events().list(calendarId=calendarId, timeMin=startDate,
                                            timeMax=stopDate,maxResults=100, singleEvents=True,
                                            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        if events:
            for event in events:
                eventStart = event['start'].get('dateTime', event['start'].get('date'))
                startTime = dateutil.parser.parse(eventStart).astimezone(LocalTimezone())
                startTimeStr = startTime.strftime('%H:%M')
                if startTimeStr != '00:00':
                    print(startTime.strftime('%H:%M'), event['summary'])
                    return time.mktime(startTime.timetuple())
        print('No upcoming events found.')
        return None

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

        service = build('calendar', 'v3', credentials=creds)
        self._service = service

    def getCalendarAlarms(self):
        calendarAlarms = []
        for calendarId in self._calendarIdList:
            startTime = self.getFirstEvent(calendarId)
            if startTime:
                calendarAlarms.append(Alarm(startTime,True,True))
        return calendarAlarms

def test():
    cal = Cal()
    for alarm in cal.getCalendarAlarms():
        print(alarm,end=' | ')

test()
