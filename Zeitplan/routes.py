from flask import render_template, request, make_response, redirect, url_for
from Zeitplan import app
from Utilities.ParseTimeTable import ParseTimeTable
from Utilities.CalendarAPI import googleCalendarAPI
from os import getenv

# Variables
ENVIRON_LOCALHOST = 'ZEITPLAN_LOCALHOST'

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

        # If the application is hosted locally, a different method is required for
        # credentials retrieval.
        # Get the localhost validation from ENVIRONMENT VARAIBLES.
        if(getenv(ENVIRON_LOCALHOST) == '1'):
            print("You are working on LocalHost!")
            resp.set_cookie('data',gca.getCredsLocalhost())
        else:
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

@app.route('/message/<title>&<messageText>')
def message(title, messageText):
    data = {'title': title, 'messageText': messageText,}
    return render_template('message.html', data=data)

@app.route('/getInfo')
def getInfo():
    try:
        resp = make_response(render_template('getInfo.html'))
        # Get creds from cookies
        creds = request.cookies.get('data',None)
        # If creds not available, then authorize
        if not creds:
            return redirect('authorize')
        return resp
    except Exception as e:
        print(f"Error in getInfo() in routes.py:\n{str(e)}\n")
        return render_template('sww.html')

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    try:
        # Decode and retrive google.oauth2.credentials.Credentials object
        creds = request.cookies.get('data',None)
        creds = gca.decodeCredentials(creds)
        gca.buildService(creds)

        if request.method=='POST':
            resp = make_response(redirect('message/Success&Events added!'))
            # Add Events
            ttInText = request.form.get('ttInText',' ')
            start_date = request.form.get('start_date',' ')
            recurEvent = request.form.get('recurringEvent',False,type=bool)
            end_date = None
            if(recurEvent):
                end_date = request.form.get('end_date',-1)
            calendarId = request.form.get('calendarId', '')
            if(calendarId==''):
                calendarId = gca.getZeitplanCalendarID()
            eventColor = request.form.get('eventColor',9,type=int)
            lectures = ptt.convertTTtoEvents(ttInText,start_date)
            # print(lst) # Debugging
            for lecture in lectures:
                gca.insertEvent(
                    calendarId,
                    gca.createRequestBody(
                        lecture[1],lecture[2],lecture[3],lecture[0],lecture[4],lecture[5],recurEvent,end_date,eventColor
                    )
                )
            # Save Calendar ID in cookies
            resp.set_cookie('calendarId', calendarId)
            return resp
        else:
            return render_template('error.html')
    except Exception as e:
        print(f'Error in routes.py: getData() => {str(e)}')
        return render_template('sww.html')

@app.route('/privacyPolicy')
def privacyPolicy():
    return render_template('privacy_policy.html')


# Routes for Responsive WebPages


'''
References:
    - https://tedboy.github.io/flask/generated/generated/werkzeug.ImmutableMultiDict.get.html#werkzeug.ImmutableMultiDict.get
    - Environment Varialbles:  https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5
'''