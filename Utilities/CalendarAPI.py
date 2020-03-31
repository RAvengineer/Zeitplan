# Imports
from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, json, Flow
from google.oauth2.credentials import Credentials

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
    
    def getCreds(self, state, ruri, auth_resp):
        flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = ruri

        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        authorization_response = auth_resp
        flow.fetch_token(authorization_response=authorization_response)
        return self.encodeCredentials(flow.credentials)
    
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
        creds = Credentials(**jcreds)
        return creds
    
    def buildService(self,creds):
        self.service = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

'''
References:
    https://gist.github.com/nikhilkumarsingh/8a88be71243afe8d69390749d16c8322
    https://developers.google.com/identity/protocols/oauth2/web-server#example
'''