from flask import render_template, request, Response,jsonify
from Zeitplan import app

# Variables


# Objects/ Instances


# Routes for Templates
@app.route('/')
@app.route('/Zeitplan')
def genesys_v2():
    return render_template('base.html')


# Routes for Responsive WebPages
