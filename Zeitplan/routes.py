from flask import render_template, request, Response,jsonify
from Zeitplan import app
from Utilities.ParseTimeTable import ParseTimeTable

# Variables


# Objects/ Instances
ptt = ParseTimeTable()

# Routes for Templates
@app.route('/')
@app.route('/Zeitplan')
def zeitplan():
    return render_template('home.html')

@app.route('/getInfo')
def getInfo():
    return render_template('getInfo.html')

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