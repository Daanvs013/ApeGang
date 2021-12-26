from functions import getClosingPrice, getLivePrice
from yahoo_fin import stock_info as si

class investor():
    def __init__(self,name,email):
        self.name = str(name)
        self.holdings = []
        self.email = email

    def changeName(self,name):
        self.name = name

    def changeEmail(self,email):
        self.email = str(email)

    def clearHoldings(self):
        self.holdings = []

    def totalValue(self,status='live'):
        totvalue = 0
        for holding in self.holdings:
            totvalue += holding.totalValue(status)
        return round(totvalue,2)

    def totalCost(self):
        cost = 0
        for holding in self.holdings:
            cost += holding.cost
        return round(cost,2)
    
    def totalProfit(self,status='live'):
        profit = 0
        for holding in self.holdings:
            profit += holding.profit(status)
        return round(profit,2)
    
    def totalRendement(self,status='live'):
        return round(100*self.totalProfit(status)/self.totalCost(),2)

    def totalShares(self):
        shares = 0
        for holding in self.holdings:
            shares += holding.shares
        return shares

    def gak(self):
        ## gak is the 'Gemiddelde Aankoop kosten'
        ## thus total amount spent devided by the total amount of shares
        return round(self.totalCost()/self.totalShares(),2)

    def addHolding(self,name,shares,price):
        found = False
        for holding in self.holdings:
            ## add shares to existing brokerage holdings
            if holding.name == name:
                found = True
                holding.addShares(shares,price)
            else:
                pass
        ## if no shares were added to any existing holdings, create new holding object
        ## price is in this case equal to gak
        if found == False:
            holding = broker(name,shares,price)
            self.holdings.append(holding)
        else:
            pass

    def __str__(self):
        output = ""
        totvalue = self.totalValue('live')
        gak = self.gak()
        for holding in self.holdings:
            output += str(holding)+"\n"
        return "------------\nNaam: "+self.name+"\n----\n"+"Aandelen: \n"+output+"----\nTotaal:\nAantal: "+str(self.totalShares())+", waarde: $"+str(totvalue)+", gak: $"+str(gak)+", winst: $"+str(self.totalProfit())+", rendement: "+str(self.totalRendement())+"%\n------------"

class broker():
    
    def __init__(self,name,shares,gak):
        self.name=str(name)
        self.shares=float(shares)
        self.gak=float(gak[0:-2])
        self.cost = float(shares)*float(gak)
    
    def changeName(self,name):
        self.name = name

    def changeHolding(self,shares,gak):
        self.shares = shares
        self.gak = gak

    def totalValue(self,status='live'):
        if status == 'live':
            value = float(self.shares) * float(getLivePrice())
        elif status == 'close':
            value = float(self.shares) * float(getClosingPrice())
        else:
            value = 0
        return round(value,2)

    def profit(self,status='live'):
        if status == 'live':
            value = float(self.shares) * float(getLivePrice())
        elif status == 'close':
            value = float(self.shares) * float(getClosingPrice())
        else:
            value = 0
        profit = value - self.cost
        return round(profit,2)

    def rendement(self,status='live'):
        if status == 'live':
            price = float(getLivePrice())
        elif status == 'close':
            price = float(getClosingPrice())
        else:
            price = 0

        return round(100*(price-self.gak)/self.gak,2)

    def addShares(self,shares,price):
        ## gak is the 'Gemiddelde Aankoop kosten' for this holding
        ## thus total amount spent devided by the total amount of shares
        newgak = (self.cost + shares*price)/(self.shares + shares)
        self.shares += shares
        self.gak = newgak

    def __str__(self):
        return "Broker: "+self.name+", aantal: "+str(self.shares)+", waarde: $"+str(self.totalValue())+", GAK: $"+str(self.gak)+", winst: $"+str(self.profit())+", rendement: "+str(self.rendement())+"%"

class group():

    def __init__(self,members):
        self.name = 'Apegang'
        self.members = members
    
    def changeName(self,name):
        self.name = name

    def clearMembers(self):
        self.members = []

    def totalShares(self):
        shares = 0
        for member in self.members:
            shares += member.totalShares()
        return shares
    
    def totalValue(self,status='live'):
        value = 0
        for member in self.members:
            value += member.totalValue(status)
        return value
    
    def totalCost(self):
        cost = 0
        for member in self.members:
            cost += member.totalCost()
        return cost
    
    def totalProfit(self,status='live'):
        profit = 0
        for member in self.members:
            profit += member.totalProfit(status)
        return profit
    
    def totalRendement(self,status='live'):
        return round(100*self.totalProfit(status)/self.totalCost(),2)

    def gak(self):
        return round(self.totalCost()/self.totalShares(),2)

    def __str__(self):
        return "Groep: "+str(self.name)+", aandelen: "+str(self.totalShares())+", waarde: $"+str(self.totalValue('live'))+", gak: $"+str(self.gak())+", winst: $"+str(self.totalProfit('live'))+", rendement:"+str(self.totalRendement('live'))+"%"

class company():

    def __init__(self):
        self.name = 'GameStop'
        self.ticker = 'GME'
        self.adres = {
            "street": "625 Westport Parkway",
            "city": "Grapevine",
            "zip": "76051",
            "state": "Texas",
            "country": "United States"
        }
        self.phone = "(817) 424 2000"

    def marketCap(self):
        outstanding_float = si.get_stats("GME").loc[10][1]
        marketcap = round(float(outstanding_float[:-1]) * float(getLivePrice())/1000,2)
        return marketcap

