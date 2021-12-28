## packages
from logging import debug
from flask.debughelpers import DebugFilesKeyError
import pandas as pd
from datetime import date
from requests.api import get
from yahoo_fin import stock_info as si
import logging
from os import path
##import sqlite3
## flask packages
from flask import Flask, render_template, url_for, request
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO, emit,send
from flask_sqlalchemy import SQLAlchemy
## import own packages
from classes import group,company,investor
from functions import getClosingPrice,getLivePrice, init, updateStats, sendEmail, getPreviousPrice
#from databases import createDatabases

##init flaskapp and scheduler
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
socketio = SocketIO(app,async_mode='threading')
## init database
##createDatabases(app)
##


clients = []
## create investor classes from csv files
investor_list = []
init(investor,investor_list)
## create group class with all investors as members
apegang = group(investor_list)
## create company class
gamestop = company()

## routes
@app.route('/home/')
@app.route('/index/')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/bram/')
def bram():
    return render_template("bram.html")

@app.route('/daan/')
def daan():
    return render_template("daan.html")

@app.route('/ernst/')
def ernst():
    return render_template("ernst.html")

@app.route('/harm/')
def harm():
    return render_template("harm.html")

@app.route('/wenting/')
def wenting():
    return render_template("wenting.html")

##socket listeners
@socketio.on('connect')
def connect():
    id = request.sid
    print("Client "+id+" verbonden met server")
    clients.append(id)
    socketio.emit('client_connect_response', id)

@socketio.on('disconnect')
def disconnect():
    id = request.sid
    clients.remove(id)
    print("Client "+id+" heeft de server verlaten")

@socketio.on('ticker_price')
def event1(data):
    gme = round(getLivePrice(),2)
    previous = getPreviousPrice()
    socketio.emit('ticker_price_response',{"price":gme,"previousprice":previous})

@socketio.on('table_data')
def event4(data):
    output = []
    for investor in investor_list:
        package = {
            "name": investor.name,
            "gak": investor.gak(),
            "shares": investor.totalShares(),
            "previousvalue":investor.previousvalue()
        }
        output.append(package)
    package = {
        "name": apegang.name,
        "gak": apegang.gak(),
        "shares": apegang.totalShares(),
        "previousvalue":apegang.previousvalue()
    }
    output.append(package)
    socketio.emit('table_data_response', output)


##schedulers
@scheduler.task('cron', id='1',week='*', day_of_week='*', hour ='22',minute='15' )
def task1():
    updateStats(investor_list,apegang)

""" @scheduler.task('cron', id='2',week='*', day_of_week='*', hour ='22',minute='10' )
def task2():
    sendEmail(investor_list,gamestop) """

## run flask app
if __name__ == '__main__':
    print('Server Starting...')
    socketio.run(app, debug=False)
