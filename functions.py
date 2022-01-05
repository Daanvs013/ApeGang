from yahoo_fin import stock_info as si
import pandas as pd
from datetime import date,datetime
import os
## email packages
import smtplib
from email.message import EmailMessage

## mongoDB
from mongo import *

def getLivePrice():
    status = si.get_market_status()
    gme = 0
    if status == 'PRE':
        gme =  si.get_premarket_price('GME')
    elif status == 'POST':
        gme =  si.get_postmarket_price("GME")
    elif status == 'REGULAR':
        gme =  si.get_live_price("GME")
    elif status == 'CLOSED':
        gme =  si.get_live_price("GME")
    return gme
    
def getClosingPrice():
    price = si.get_live_price("GME")
    return price

def getPreviousPrice():
    post = collection_price.find().sort('dag',-1)
    previousprice = post[0]["sluitkoers"]
    return float(previousprice)

def updateStats():
    for member in collection_members.find({}):
        name = member["naam"]
        for holding in member["holdings"]:
            ##print(name+"+"+holding)
            db = cluster[name]
            collection = db[holding].find().sort('dag',-1)

            day = datetime.today()
            value = float(collection[0]["aantal"] * getClosingPrice())
            previousvalue = float(collection[1]["waarde"])
            change = float(value - previousvalue)
            relchange = 0
            if previousvalue != 0:
                relchange = round(100*change/previousvalue,2)
            cost = float(collection[0]["aantal"] * collection[0]["gak"])
            profit = round(value-cost,2)
            rendement = 0
            if cost !=0:
                rendement = round(100*profit/cost,2)
            ## update 
            db[holding].update_one({"dag":{"$gte":datetime(day.year,day.month,day.day)}},{"$set": {
                "waarde":round(value,2),
                "verandering":round(change,2),
                "%verandering":relchange,
                "winst": profit,
                "rendement": rendement
            }})

    ## total
    collection = collection_totaal.find().sort('dag',-1)
    day = datetime.today()
    value = float(collection[0]["aantal"] * getClosingPrice())
    previousvalue = float(collection[1]["waarde"])
    change = float(value - previousvalue)
    relchange = 0
    if previousvalue != 0:
        relchange = round(100*change/previousvalue,2)
    cost = float(collection[0]["aantal"] * collection[0]["gak"])
    profit = round(value-cost,2)
    rendement = 0
    if cost !=0:
        rendement = round(100*profit/cost,2)
    ## update 
    collection_totaal.update_one({"dag":{"$gte":datetime(day.year,day.month,day.day)}},{"$set": {
        "waarde":round(value,2),
        "verandering":round(change,2),
        "%verandering":relchange,
        "winst": profit,
        "rendement": rendement
    }})

    ## koers
    collection = collection_price.find().sort('dag',-1)
    previousprice = collection[0]['sluitkoers']
    price = getClosingPrice()
    change = float(price - previousprice)
    relchange = round(100*change/previousprice,2)
    volume = 5
    collection_price.insert_one({
        "dag":day,
        "sluitkoers": round(price,2),
        "verandering": round(change,2),
        "%verandering": relchange,
        "volume": volume
    })

def insertDay():
    for member in collection_members.find({}):
        name = member["naam"]
        for holding in member["holdings"]:
            ##print(name+"+"+holding)
            db = cluster[name]
            collection = db[holding].find().sort('dag',-1)

            day = datetime.today()
            ## insert new
            db[holding].insert_one({
                "dag":day,
                "waarde":0,
                "verandering":0,
                "%verandering":0,
                "winst":0,
                "rendement":0,
                "aantal":collection[0]["aantal"],
                "gak":collection[0]["gak"]
            })
    ## total
    collection = collection_totaal.find().sort('dag',-1)

    day = datetime.today()
    ## insert new
    collection_totaal.insert_one({
        "dag":day,
        "waarde":0,
        "verandering":0,
        "%verandering":0,
        "winst":0,
        "rendement":0,
        "aantal":collection[0]["aantal"],
        "gak":collection[0]["gak"]
    })

def sendEmail(investor_list,gamestop):
    ## get login details
    with open('login.txt','r') as f:
        lines = f.readlines()
        f.close()
    LOGIN_EMAIL = lines[0]
    LOGIN_PASSWORD = lines[1]

    for investor in investor_list:
        file = str(investor.name)+".csv"
        name = investor.name
        ## open dataframe
        data = pd.read_csv("CSV/"+file)
        df = pd.DataFrame(data)

        ## open dataframe2
        data2 = pd.read_csv("CSV/Price.csv")
        df2 = pd.DataFrame(data2)

        msg = EmailMessage()

        wordlist = []
        currentdate = df.loc[0][0]
        value = df.loc[0][1]
        change = df.loc[0][2]
        if float(change) < 0:
            wordlist.append('red')
            wordlist.append('minder')
        else:
            wordlist.append('green')
            wordlist.append('meer')
        relchange = df.loc[0][3]
        profit = df.loc[0][4]
        if float(profit) < 0:
            wordlist.append('red')
        else: 
            wordlist.append('green')
        price = df2.loc[0][1]
        pricechange = df2.loc[0][2]
        relpricechange = df2.loc[0][3]
        volume = df2.loc[0][4]
        if float(pricechange) < 0:
            wordlist.append('red')
        else:
            wordlist.append('green')
        rendement = df.loc[0][5]
        shares = df.loc[0][6]
        totshares = 0
        for investor in investor_list:
            totshares += investor.totalShares()
        percentage = round(100*shares/totshares,2)
        totvalue = round(totshares * getClosingPrice(),2)
        gak = df.loc[0][7]
        marketcap = gamestop.marketCap()

        msg['Subject'] = 'ApeGang Daily | '+str(currentdate)+' | '+str(relchange)+'%'
        msg['From'] = 'd.l.n.v.apegang@gmail.com'
        msg['To'] = str(investor.email)

        msg.add_alternative(""" 
        <div style="text-align:center">  <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Flogodix.com%2Flogo%2F318146.png&amp;f=1&amp;nofb=1"
        width="50%" height="auto"> <br> Hoi """+str(name)+""", hier is je dagelijkse update over je GameStop investering.<br><br><br>De koers is vandaag met 
        <span style="color:"""+str(wordlist[3])+"""">"""+str(pricechange)+"""</span>$ gestegen naar """+str(price)+"""$.<br> Dit is een procentuele verandering van 
        <span style="color:"""+str(wordlist[3])+"""">"""+str(relpricechange)+"""</span>%.<br> Er zijn vandaag """+str(volume)+""" miljoen aandelen verhandeld op de markt.<br><br>Je portfolio 
        is nu """+str(value)+"""$ waard.<br>Dit is <span style="color:"""+str(wordlist[0])+"""">"""+str(change)+"""</span>$ """+str(wordlist[1])+""" dan gisteren.<br>De procentuele verandering is
        <span style="color:"""+str(wordlist[0])+"""">"""+str(relchange)+"""</span>%.<br> Je hebt vandaag 0 aandelen gekocht.<br><br>Je Gemiddelde Aankoop Prijs is """+str(gak)+"""$.<br> 
        Hierdoor is je totale winst nu <span style="color:"""+str(wordlist[2])+"""">"""+str(profit)+"""</span>$.<br> Dit is een rendement van <span style="color:"""+str(wordlist[2])+"""">
        """+str(rendement)+"""</span>%<br><br> De totale waarde van de ApeGang is nu """+str(totvalue)+"""$, jij hebt hier """+str(percentage)+"""% van.<br> 
        Je hebt """+str(shares)+""" aandelen <br>Vandaag zijn er 0 aandelen gekocht door de ApeGang.<br><br>GameStop heeft een marktwaarde van """+str(marketcap)+"""$ miljard
        <br><br><br><br><span style="font-size:0.8em">Deze email is automatisch verzonden door het nieuwe Python script, wil je hem niet meer ontvangen?
        Stuur dan een bericht naar Daan</span></div>""", subtype='html')

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(LOGIN_EMAIL, LOGIN_PASSWORD)
            print('emailsend')
            smtp.send_message(msg)
