from numpy.core import getlimits
import pandas as pd
import time
import schedule
import threading
from datetime import date, datetime
import smtplib
from email.message import EmailMessage


from requests.api import get
from classes import investor,group,company
from functions import getClosingPrice,getLivePrice
investor_list = []

## read data file
with open('CSV/data.csv', 'r') as f:
    lines = f.readlines()
    f.close()

## create investor objects
## search for 'name=' syntax
for line in lines:
    if line.startswith("name="):
        text = line.split(sep=",")
        email = text[2][7:-2]
        name = investor(str(text[0][5:]),email)
        investor_list.append(name)
        ## check how many initial holdings that investor has
        holdings = text[1][9:]
        start = lines.index(line) + 1
        end = start+int(holdings)
        ## add all holdings to the investor object
        for j in range(start,end):
            text = lines[j].split(sep=",")
            name.addHolding(text[0],text[1],text[2])
    else:
        pass
## create group object with all investors as members
apegang = group(investor_list)
## create company object
gamestop = company()



def updateStats():
    for investor in investor_list:
        name = str(investor.name)+".csv"
        ## open dataframe
        data = pd.read_csv("CSV/"+name)
        df = pd.DataFrame(data)
        ## columns
        currentdate = date.today().strftime("%d/%m/%Y")
        value = investor.totalValue('live')
        previous_value = df.loc[0][1]
        change = round(value - previous_value)
        relchange = round(100*change/previous_value,2)
        profit = investor.totalProfit('live')
        rendement = investor.totalRendement('live')
        shares = investor.totalShares()
        gak = investor.gak()
        cost = investor.totalCost()
        ## add row to dataframe
        row = pd.Series([currentdate,value,change,relchange,profit,rendement,shares,gak,cost], index=df.columns)
        df.loc[-1] = row
        df.index = df.index + 1
        df = df.sort_index()
        ## save new dataframe to file
        print(df)
        df.to_csv("CSV/"+name, index=False)
    
def updatePrice():
    ## open dataframe
    data = pd.read_csv("CSV/Price.csv")
    df = pd.DataFrame(data)
    ## columns
    currentdate = date.today().strftime("%d/%m/%Y")
    price = getClosingPrice()
    previousprice = float(df.loc[0][1])
    change = price - previousprice
    relchange = round(100*(change/previousprice),2)
    volume = 0
    ## add row to dataframe
    row = pd.Series([currentdate,price,change,relchange,volume], index=df.columns)
    df.loc[-1] = row
    df.index = df.index + 1
    df = df.sort_index()
    ## save new dataframe to file
    print(df)
    df.to_csv("CSV/Price.csv", index=False)

def sendEmail():
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

def ticker():
    time = datetime.now().strftime("%H:%M:%S")
    print(time)
    print("Koers GME: $"+str(round(getLivePrice(),2)))
    for x in investor_list:
        print(x.name+": $"+str(x.totalValue('live')))
    print("----------------------------")

## run function in parallel to main.py with the module 'threading'
def run_threaded(function):
    function = threading.Thread(target=function)
    function.start()

##schedules
schedule.every(10).seconds.do(run_threaded,ticker)
schedule.every().monday.at("22:30").do(run_threaded,sendEmail)
schedule.every().monday.at("22:20").do(run_threaded,updateStats)
schedule.every().monday.at("22:19").do(run_threaded,updatePrice)
schedule.every().tuesday.at("22:30").do(run_threaded,sendEmail)
schedule.every().tuesday.at("22:20").do(run_threaded,updateStats)
schedule.every().tuesday.at("22:19").do(run_threaded,updatePrice)
schedule.every().wednesday.at("22:30").do(run_threaded,sendEmail)
schedule.every().wednesday.at("22:20").do(run_threaded,updateStats)
schedule.every().wednesday.at("22:19").do(run_threaded,updatePrice)
schedule.every().thursday.at("22:30").do(run_threaded,sendEmail)
schedule.every().thursday.at("22:20").do(run_threaded,updateStats)
schedule.every().thursday.at("22:19").do(run_threaded,updatePrice)
schedule.every().friday.at("22:30").do(run_threaded,sendEmail)
schedule.every().friday.at("22:20").do(run_threaded,updateStats)
schedule.every().friday.at("22:19").do(run_threaded,updatePrice)

## loop
loop = True
while loop:
    schedule.run_pending()
    time.sleep(1)