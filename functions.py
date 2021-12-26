from yahoo_fin import stock_info as si

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

def init(investor, investor_list):
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
