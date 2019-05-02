import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Delete file token.pickle when modifying scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def tokenGenerator():
    while(True):
        if os.path.exists('token.pickle'):
            print('Logged in.')
            str = input('Do you want to change user? (yes/close)\n')
        else:
            print('Not logged in.')
            str = input('Do you want to log in? (yes/close)\n')
        if str.lower() == 'yes':
            newCreds()
        elif str.lower() == 'close':
            break

def newCreds(): # init credentials and connect to new google account
    # let the user log in
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

tokenGenerator()
