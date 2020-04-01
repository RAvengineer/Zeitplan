# Imports
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, json, Flow
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

# This variable specifies the name of a file that contains the OAuth 2.0
# information for this application, including its client_id and client_secret.
CLIENT_SECRETS_FILE = "/home/RAvengineer/Zeitplan/Utilities/client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
API_SERVICE_NAME = 'calendar'
API_VERSION = 'v3'

class googleCalendarAPI():
    def __init__(self):
        '''
        Constructor for googleCalendarAPI
        '''
        self.service = None
    
    def getAuthorizationUrl(self,ruri):
        try:
            # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
            flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)

            # The URI created here must exactly match one of the authorized redirect URIs
            # for the OAuth 2.0 client, which you configured in the API Console. If this
            # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
            # error.
            flow.redirect_uri = ruri

            authorization_url, state = flow.authorization_url(
                # Enable offline access so that you can refresh an access token without
                # re-prompting the user for permission. Recommended for web server apps.
                access_type='offline',
                # Enable incremental authorization. Recommended as a best practice.
                include_granted_scopes='true')
            return (authorization_url, state)
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: getAuthorizationUrl(): {str(e)}")
    
    def getCreds(self, state, ruri, auth_resp):
        try:
            flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
            flow.redirect_uri = ruri

            # Use the authorization server's response to fetch the OAuth 2.0 tokens.
            authorization_response = auth_resp
            flow.fetch_token(authorization_response=authorization_response)
            return self.encodeCredentials(flow.credentials)
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: getCreds(): {str(e)}")
    
    def encodeCredentials(self, creds):
        try:
            return creds.to_json().encode()
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: encodeCredentials(): {str(e)}")
    
    def decodeCredentials(self, json_creds):
        try:
            jcreds = json.loads(json_creds)
            creds = Credentials(**jcreds)
            return creds
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: decodeCredentials(): {str(e)}")
    
    def buildService(self,creds):
        try:
            self.service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: buildService(): {str(e)}")
    
    def createRequestBody(self, title, location, desc, start_dt, duration, popup_duration=10, recur=False,until_dt=None,color=9):
        '''
        Creates the Request Body 'event' to be added into the calendar\n
        The Recurring Event is default WEEKLY\n
        TimeZone: 'Asia/Kolkata'\n
        Parameters:
            title: str :- Title of the Event
            location: str :- Location of the Event
            desc: str :- Description
            start_dt: datetime obj :- Start Time of the Event
            duration: int (in minutes) :- Duration of the Event
            popup_duration:
                int :- Notification Time(in minutes)
                default = 10
            recur: boolean :- Is this recurring event?
                default = False
            until_dt: datetime obj :- End Date for Recurring Event
                default = None
            color: int [1-11] both inclusive :- Decides the color for the Event
                default = 9
        Returns:
            dict
        '''
        try:
            start_time = start_dt
            end_time = start_time + timedelta(minutes=duration)
            timezone = 'Asia/Kolkata'
            colorId = str(color)
            requestBody = {
                'summary': title,
                'location': location,
                'description': desc,
                'start': {
                    'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': popup_duration},
                    ],
                },
                'colorId':colorId,
            }
            if(recur):
                requestBody['recurrence'] = ['RRULE:FREQ=WEEKLY;UNTIL='+until_dt.strftime("%Y%m%dT000000Z")]
            return requestBody
        except Exception as e:
            raise Exception(f"Error in CalendarAPI.py: createRequestBody(): {str(e)}")


'''
References:
    https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
    https://developers.google.com/identity/protocols/oauth2/web-server#example
'''