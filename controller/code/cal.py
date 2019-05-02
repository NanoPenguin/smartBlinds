from __future__ import print_function
import datetime
import dateutil.parser
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from tz import LocalTimezone

#Delete file token.pickle when modifying scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
class Cal():
    def __init__(self,calendarId=None):
        self.__calendarIdList = []
        self.initCreds()
        if calendarId:
            self.__calendarIdList.append(calendarId)
        self.loadCalendarIds()



    def loadCalendarIds(self):
        calendarList = self.__service.calendarList().list().execute()
        for calendar in calendarList['items']:
            self.__calendarIdList.append(calendar['id'])


    def getFirstEvent(self,calendarId):
        # Call the Calendar API
        print('Getting the upcoming morning event')
        currentTime = datetime.datetime.utcnow()
        dt = currentTime.replace(day=currentTime.day+1,hour=0,minute=0,second=0)
        startDate = dt.isoformat()+'Z'
        #8vu3do178lqo3rk17seb5uhgmdlgl53v@import.calendar.google.com
        events_result = self.__service.events().list(calendarId=calendarId, timeMin=startDate,
                                            maxResults=1, singleEvents=True,
                                            orderBy='startTime').execute()
        event = events_result.get('items', [])[0]

        if not event:
            print('No upcoming events found.')
        else:
            eventStart = event['start'].get('dateTime', event['start'].get('date'))
            startTime = dateutil.parser.parse(eventStart)
            startTime = startTime.astimezone(LocalTimezone())
            startTime = startTime.strftime('%H:%M')
            print(startTime, event['summary'])

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
        self.__service = service

    def getCalendarAlarms(self):
        calendarAlarms = []
        for calendarId in self.__calendarIdList:
            calendarAlarms.append(Alarm(getFirstEvent(calendarId),True,True))
        return calendarAlarms

def test():
    cal = Cal()
    print(cal.getCalendarAlarms())

test()
