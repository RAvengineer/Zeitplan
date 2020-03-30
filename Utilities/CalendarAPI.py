# Imports
from google_auth_oauthlib.flow import InstalledAppFlow

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
    