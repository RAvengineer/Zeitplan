from flask import render_template, request, Response,jsonify
from Zeitplan import app

# Variables


# Objects/ Instances


# Routes for Templates
@app.route('/')
@app.route('/Zeitplan')
def zeitplan():
    return render_template('getInfo.html')

@app.route('/getData', methods=['GET', 'POST'])
def getData():
    if request.method=='POST':
        print(request.form['ttInText'])
        return render_template('getInfo.html')
    else:
        return render_template('error.html')


# Routes for Responsive WebPages
