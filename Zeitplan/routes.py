from flask import render_template, request, Response,jsonify, make_response
from Zeitplan import app
from Utilities.ParseTimeTable import ParseTimeTable
from Utilities.CalendarAPI import googleCalendarAPI
from google.auth.transport.requests import Request

# Variables


# Objects/ Instances
ptt = ParseTimeTable()
gca = googleCalendarAPI()

# Routes for Templates
@app.route('/')
@app.route('/Zeitplan')
def zeitplan():
    return render_template('home.html')

@app.route('/getInfo')
def getInfo():
    try:
        resp = make_response(render_template('getInfo.html'))
        # Get creds from cookies
        creds = request.cookies.get('data',None)

        # Decode and retrive google.oauth2.credentials.Credentials object, 
        # if creds available in cookies
        if creds:
            creds = gca.decodeCredentials(creds)
        
        # If creds not avalaible in cookies or creds not valid
        if not creds or not creds.valid:
            # If creds available, and creds is expired and refresh_token is available
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Generate keys, if creds not available
                creds = gca.generateAPIkey()
            # Add the new keys to the cookies
            resp.set_cookie('data',gca.encodeCredentials(creds))
        return resp
    except Exception as e:
        print(f"Error in getInfo() in routes.py:\n{str(e)}\n")
        return render_template('sww.html')

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    if request.method=='POST':
        ttInText = request.form.get('ttInText',' ')
        start_date = request.form.get('start_date',' ')
        if(request.form.get('recurringEvent',False,type=bool)):
            end_date = request.form.get('end_date',-1)
        calendarId = request.form.get('calendarId',"primary")
        if(calendarId==''):
            calendarId = "primary"
        lst = ptt.convertTTtoEvents(ttInText,start_date)
        # print(lst) # Debugging
        print(lst)
        if(lst==-1):
            return render_template('sww.html')
        return render_template('getInfo.html')
    else:
        return render_template('error.html')


# Routes for Responsive WebPages


'''
References:
https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.get.html#werkzeug.ImmutableMultiDict.get
'''