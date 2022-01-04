// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_daan','all')
});

//ticker_price
socket.on('ticker_price_response', function(data){
    //console.log(data)
    var table = document.getElementById('table');
    price = data.price
    document.getElementById("ticker_price").innerHTML = price;
    change = price - data.previousprice
    relchange = 100*(change)/data.previousprice
    if(change<0){
        document.getElementById("ticker_change").style.color = 'red';
        document.getElementById("ticker_change").innerHTML = `${round(change,2)} ( ${round(relchange,2)}% )`;
    } else {
        document.getElementById("ticker_change").style.color = '#009879';
        document.getElementById("ticker_change").innerHTML = `+${round(change,2)} ( ${round(relchange,2)}% )`;
    }

    if(table_list == []){
        
    } else {
        table_list.forEach((broker) => {
            row = 0
            //console.log(broker)
            if(broker.name == 'Degiro'){
                row = 1
            } else if(broker.name == 'Rabobank'){
                row = 2
            } else if(broker.name == 'IBKR'){
                row = 3
            } else if(broker.name == 'ComputerShare'){
                row = 4
            } else if(broker.name == 'Totaal'){
                row = 5
            }
            //current value
            value = broker.shares*price;
            table.rows[row].cells[1].innerHTML = round(value,2)
            //daily change and relchange
            change = value - broker.previousvalue;
            relchange = 100*(change/broker.previousvalue);
            if(change<0){
                table.rows[row].cells[2].style.color = 'red'
                table.rows[row].cells[3].style.color = 'red'
            } else {
                table.rows[row].cells[2].style.color = '#009879';
                table.rows[row].cells[3].style.color = '#009879';
            }
            table.rows[row].cells[2].innerHTML = round(change,2);
            table.rows[row].cells[3].innerHTML = round(relchange,2);
            //profit and rendement
            cost = broker.shares*broker.gak
            profit = value-cost
            rendement = 100*profit/cost
            if(profit<0){
                table.rows[row].cells[4].style.color = 'red'
                table.rows[row].cells[5].style.color = 'red'
            } else {
                table.rows[row].cells[4].style.color = '#009879';
                table.rows[row].cells[5].style.color = '#009879';
            }
            table.rows[row].cells[4].innerHTML = round(profit,2)
            table.rows[row].cells[5].innerHTML = round(rendement,2)
            //number of shares
            table.rows[row].cells[6].innerHTML = broker.shares;
            //gak
            table.rows[row].cells[7].innerHTML = broker.gak;
            //cost
            table.rows[row].cells[8].innerHTML = round(cost,2);
        });
    }
    
});
//

//table_data
table_list = []
socket.on('table_data_daan_response', function(data){
    table_list = []
    data.forEach( (broker) => {
        pack = {
            "name":broker.name,
            "shares": broker.shares,
            "gak": broker.gak,
            "previousvalue": broker.previousvalue
        }
        //console.log(pack)
        table_list.push(pack)
    });
    //console.log(table_list)
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','True')
}, 5000); 
//