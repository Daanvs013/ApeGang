import collections
import pandas as pd
import pymongo
from pymongo import MongoClient
import datetime
cluster = MongoClient("mongodb+srv://ArchdukeDaan:T384h5311m2001@apegang.mrems.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def convert_koers():
    ## open dataframe
    data = pd.read_csv("CSV/ApeGangKoers.csv")
    df = pd.DataFrame(data)
    df.pop("Hoogste")
    df.pop("Laagste")
    df.pop("Verandering per 1M volume")
    df.pop("% Verandering per 1M volume")
    df.pop("Sluit koers tov intraday Hoogste")
    print(df)
    df.to_csv("CSV/ApeGangKoers.csv", index=False)
##convert_koers()

def add_koers():
    db = cluster['GameStop']
    collection = db['Price']
    ## open dataframe
    data = pd.read_csv("CSV/ApeGangKoers.csv")
    df = pd.DataFrame(data)
    for id,row in df.iterrows():
        sluitkoers = row['$Koers'].replace(",",".")
        verandering = row['Verandering'].replace(",",".")
        relverandering = row['% verandering'].replace(",",".")
        volume = row['Volume'].replace(",",".")
        post = {
            "dag":row['Dag'],
            "sluitkoers":float(sluitkoers),
            "verandering":float(verandering),
            "%verandering":float(relverandering),
            "volume":float(volume),
        }
        print(post)
        collection.insert_one(post)
##add_koers()

def add():
    db = cluster['Totaal']
    collection = db['Totaal']
    day = datetime.datetime.today()
    post = {
        "dag":day,
        "waarde":0,
        "verandering":0,
        "%verandering":0,
        "winst":0,
        "rendement":0,
        "aantal":269.2058,
        "gak":189.39,
    }
    print(post)
    collection.insert_one(post)
add()



