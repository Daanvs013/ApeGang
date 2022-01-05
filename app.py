## packages
from logging import debug
from flask.debughelpers import DebugFilesKeyError
import pandas as pd
from datetime import date
from requests.api import get
from yahoo_fin import stock_info as si
import logging
import os
## flask packages
from flask import Flask, render_template, url_for, request, session
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO, emit,send
## mongoDB
import pymongo
from mongo import *
## import own packages
from functions import getClosingPrice,getLivePrice, insertDay, updateStats, sendEmail, getPreviousPrice

##init flaskapp and scheduler
app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.config['SECRET_KEY'] = 'key'
##os.environ['SECRET_KEY']
socketio = SocketIO(app,async_mode='threading')

clients = []

## routes
@app.route('/home/')
@app.route('/index/')
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/edit/')
def edit():
    return render_template("edit.html")

@app.route('/bram/')
def bram():
    return render_template("bram/bram.html")

@app.route('/bram/degiro/')
def bram_degiro():
    return render_template("bram/degiro.html")

@app.route('/bram/ibkr/')
def bram_ibkr():
    return render_template("bram/ibkr.html")

@app.route('/bram/computershare/')
def bram_cs():
    return render_template("bram/computershare.html")

@app.route('/bram/totaal/')
def bram_totaal():
    return render_template("bram/totaal.html")

@app.route('/daan/')
def daan():
    return render_template("daan/daan.html")

@app.route('/daan/degiro/')
def daan_degiro():
    return render_template("daan/degiro.html")

@app.route('/daan/rabobank/')
def daan_rabobank():
    return render_template("daan/rabobank.html")

@app.route('/daan/ibkr/')
def daan_ibkr():
    return render_template("daan/ibkr.html")

@app.route('/daan/computershare/')
def daan_cs():
    return render_template("daan/computershare.html")

@app.route('/daan/totaal/')
def daan_totaal():
    return render_template("daan/totaal.html")

@app.route('/ernst/')
def ernst():
    return render_template("ernst/ernst.html")

@app.route('/ernst/degiro/')
def ernst_degiro():
    return render_template("ernst/degiro.html")

@app.route('/ernst/totaal/')
def ernst_totaal():
    return render_template("ernst/totaal.html")

@app.route('/harm/')
def harm():
    return render_template("harm/harm.html")

@app.route('/harm/degiro/')
def harm_degiro():
    return render_template("harm/degiro.html")

@app.route('/harm/totaal/')
def harm_totaal():
    return render_template("harm/totaal.html")

@app.route('/wenting/')
def wenting():
    return render_template("wenting/wenting.html")

@app.route('/wenting/degiro/')
def wenting_degiro():
    return render_template("wenting/degiro.html")

@app.route('/wenting/totaal/')
def wenting_totaal():
    return render_template("wenting/totaal.html")

@app.route('/totaal/')
def totaal():
    return render_template("totaal.html")

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
    socketio.emit('ticker_price_response',{"price":gme,"previousprice":previous,"sender":data})

@socketio.on('table_data_index')
def event4(data):
    output = []
    ## bram
    post = collection_bram_totaal.find().sort('dag',-1)
    package = {
        "name": "Bram",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##daan
    post = collection_daan_totaal.find().sort('dag',-1)
    package = {
        "name": "Daan",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ## ernst
    post = collection_ernst_totaal.find().sort('dag',-1)
    package = {
        "name": "Ernst",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ## harm
    post = collection_harm_totaal.find().sort('dag',-1)
    package = {
        "name": "Harm",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ## wenting
    post = collection_wenting_totaal.find().sort('dag',-1)
    package = {
        "name": "Wenting",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ## totaal
    post = collection_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("table_data_daan")
def event5(data):
    output = []
    ##degiro
    post = collection_daan_degiro.find().sort('dag',-1)
    package = {
        "name": "Degiro",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##rabobank
    post = collection_daan_rabobank.find().sort('dag',-1)
    package = {
        "name": "Rabobank",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##ibkr
    post = collection_daan_ibkr.find().sort('dag',-1)
    package = {
        "name": "IBKR",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##cs
    post = collection_daan_cs.find().sort('dag',-1)
    package = {
        "name": "ComputerShare",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##totaal
    post = collection_daan_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("table_data_bram")
def event6(data):
    output = []
    ##degiro
    post = collection_bram_degiro.find().sort('dag',-1)
    package = {
        "name": "Degiro",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##ibkr
    post = collection_bram_ibkr.find().sort('dag',-1)
    package = {
        "name": "IBKR",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##cs
    post = collection_bram_cs.find().sort('dag',-1)
    package = {
        "name": "ComputerShare",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##totaal
    post = collection_bram_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("table_data_ernst")
def event7(data):
    output = []
    ##degiro
    post = collection_ernst_degiro.find().sort('dag',-1)
    package = {
        "name": "Degiro",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##totaal
    post = collection_ernst_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("table_data_harm")
def event8(data):
    output = []
    ##degiro
    post = collection_harm_degiro.find().sort('dag',-1)
    package = {
        "name": "Degiro",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##totaal
    post = collection_harm_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("table_data_wenting")
def event9(data):
    output = []
    ##degiro
    post = collection_wenting_degiro.find().sort('dag',-1)
    package = {
        "name": "Degiro",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    ##totaal
    post = collection_wenting_totaal.find().sort('dag',-1)
    package = {
        "name": "Totaal",
        "gak": post[0]["gak"],
        "shares": post[0]["aantal"],
        "previousvalue":post[1]["waarde"]
    }
    output.append(package)
    socketio.emit('table_data_response', output)

@socketio.on("history_table")
def event10(data):
    ##print("sender"+data[0]+" broker"+data[1]+" hoeveelheid"+str(data[2]))
    output = []
    sender = data[0]
    broker = data[1]
    amount = data[2]
    if sender == 'Totaal':
        post = collection_totaal.find().sort('dag',-1)
    elif sender == 'Price':
        post = collection_price.find().sort('dag',-1)
    else:
        post = cluster[sender][broker].find().sort('dag',-1)
    for entry in post[1:]:
        if amount < 1:
            break
        else:
            package = {
                "day": str(entry["dag"]),
                "value":entry["waarde"],
                "change":entry["verandering"],
                "relchange":entry["%verandering"],
                "profit":entry["winst"],
                "rendement":entry["rendement"],
                "gak":entry["gak"],
                "shares":entry["aantal"]
            }
            output.append(package)
            ##amount = amount -1
    socketio.emit("history_table_response", output)  

@socketio.on("console")
def event10(data):
    if data == 'live':
        price = getLivePrice()
        socketio.emit("console_response","Realtime-koers: $"+str(price))
    elif data == 'end':
        price = getClosingPrice()
        socketio.emit("console_response","Sluitkoers van vandaag: $"+str(price))
    else:
        socketio.emit("console_response","Onbekend commando")

##schedulers
@scheduler.task('cron', id='1',week='*', day_of_week='*', hour ='22',minute='30' )
def task1():
    updateStats()

@scheduler.task('cron', id='2',week='*', day_of_week='*', hour ='00',minute='02' )
def task1():
    insertDay()

""" @scheduler.task('cron', id='2',week='*', day_of_week='*', hour ='22',minute='10' )
def task2():
    sendEmail(investor_list,gamestop) """

## run flask app
if __name__ == '__main__':
    print('Server Starting...')
    socketio.run(app,host='192.168.2.11',port='5000', debug=False)