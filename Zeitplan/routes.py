from flask import render_template, request, Response,jsonify, make_response, redirect, url_for
from Zeitplan import app
from Utilities.ParseTimeTable import ParseTimeTable
from Utilities.CalendarAPI import googleCalendarAPI
from google.auth.transport.requests import Request

# Variables


# Objects/ Instances
ptt = ParseTimeTable()
gca = googleCalendarAPI()

# Helper Functions and Routes
@app.route('/authorize')
def authorize():
    try:
        authorization_url, state = gca.getAuthorizationUrl(url_for('oauth2callback', _external=True))
        resp = make_response(redirect(authorization_url))
        # Store the state so the callback can verify the auth server response.
        resp.set_cookie('state', state)
        return resp
    except Exception as e:
        print(f"Error in routes.py: authorize(): {str(e)}")
        return render_template('sww.html')

@app.route('/oauth2callback')
def oauth2callback():
    try:
        resp = make_response(redirect(url_for('getInfo')))
        # Specify the state when creating the flow in the callback so that it can
        # verified in the authorization server response.
        state = request.cookies.get('state',None)

        resp.set_cookie('data',gca.getCreds(
            state,url_for('oauth2callback', _external=True),request.url))

        return resp
    except Exception as e:
        print(f"Error in routes.py: oauth2callback(): {str(e)}")
        return render_template('sww.html')

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
        # If creds not available, then authorize
        if not creds:
            return redirect('authorize')
        # Decode and retrive google.oauth2.credentials.Credentials object, 
        # if creds available in cookies
        creds = gca.decodeCredentials(creds)

        gca.buildService(creds)
        return resp
    except Exception as e:
        print(f"Error in getInfo() in routes.py:\n{str(e)}\n")
        return render_template('sww.html')

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    try:
        if request.method=='POST':
            ttInText = request.form.get('ttInText',' ')
            start_date = request.form.get('start_date',' ')
            if(request.form.get('recurringEvent',False,type=bool)):
                end_date = request.form.get('end_date',-1)
            calendarId = request.form.get('calendarId',"primary")
            if(calendarId==''):
                calendarId = "primary"
            eventColor = request.form.get('eventColor',9,type=int)
            lst = ptt.convertTTtoEvents(ttInText,start_date)
            # print(lst) # Debugging
            print(lst)
            return render_template('getInfo.html')
        else:
            return render_template('error.html')
    except Exception as e:
        print(f'Error in routes.py: getData() => {str(e)}')
        return render_template('sww.html')
   


# Routes for Responsive WebPages


'''
References:
https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.get.html#werkzeug.ImmutableMultiDict.get
'''