# Imports
from google_auth_oauthlib.flow import InstalledAppFlow, json
from google.oauth2.credentials import Credentials

class googleCalendarAPI():
    def __init__(self):
        '''
        Constructor for googleCalendarAPI
        '''
        self.service = None
    
    def generateAPIkey(self):
        try:
            SCOPES = ['https://www.googleapis.com/auth/calendar.events']
            # SCOPES = ['https://www.googleapis.com/auth/calendar']
            flow = InstalledAppFlow.from_client_secrets_file('Utilities/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            return creds
        except Exception as e:
            raise(Exception(f'Error in generateAPIkey of googleCalendarAPI creds creation:\n{str(e)}'))
    
    def encodeCredentials(self, creds):
        return creds.to_json().encode()
    
    def decodeCredentials(self, json_creds):
        jcreds = json.loads(json_creds)
        creds = Credentials(
            token=jcreds['token'],
            refresh_token=jcreds['refresh_token'],
            token_uri=jcreds['token_uri'],
            client_id=jcreds['client_id'],
            client_secret=jcreds['client_secret'],
            scopes=jcreds['scopes']
        )
        return creds