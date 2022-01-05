from pymongo import MongoClient
from datetime import datetime
import os
## clusters
cluster = MongoClient("mongodb+srv://ArchdukeDaan:T384h5311m2001@apegang.mrems.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
## databases
db_gamestop = cluster['GameStop']
db_bram = cluster['Bram']
db_daan = cluster['Daan']
db_ersnt = cluster['Ernst']
db_harm = cluster['Harm']
db_wenting = cluster['Wenting']
db_totaal = cluster["Totaal"]
## tables
collection_price = db_gamestop['Price']
collection_members = db_gamestop['Members']

collection_daan_totaal = db_daan['Totaal']
collection_daan_degiro = db_daan['Degiro']
collection_daan_ibkr = db_daan['IBKR']
collection_daan_rabobank = db_daan['Rabobank']
collection_daan_cs = db_daan['ComputerShare']

collection_bram_totaal = db_bram['Totaal']
collection_bram_degiro = db_bram['Degiro']
collection_bram_ibkr = db_bram['IBKR']
collection_bram_cs = db_bram['ComputerShare']

collection_ernst_totaal = db_ersnt['Totaal']
collection_ernst_degiro = db_ersnt['Degiro']

collection_harm_totaal = db_harm['Totaal']
collection_harm_degiro = db_harm['Degiro']

collection_wenting_totaal = db_wenting['Totaal']
collection_wenting_degiro = db_wenting['Degiro']

collection_totaal = db_totaal["Totaal"]