// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data','all')
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
        table_list.forEach((person) => {
            row = 0
            //console.log(person)
            if(person.name == 'Bram'){
                row = 1
            } else if(person.name == 'Daan'){
                row = 2
            } else if(person.name == 'Ernst'){
                row = 3
            } else if(person.name == 'Harm'){
                row = 4
            } else if(person.name == 'Wenting'){
                row = 5
            } else if(person.name == 'Apegang'){
                row = 6
            } 
            //current value
            value = person.shares*price;
            table.rows[row].cells[1].innerHTML = round(value,2)
            //daily change and relchange
            change = value - person.previousvalue;
            relchange = 100*(change/person.previousvalue);
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
            cost = person.shares*person.gak
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
            table.rows[row].cells[6].innerHTML = person.shares;
            //gak
            table.rows[row].cells[7].innerHTML = person.gak;
            //cost
            table.rows[row].cells[8].innerHTML = round(cost,2);
        });
    }
    
});
//

//table_data
table_list = []
socket.on('table_data_response', function(data){
    table_list = []
    data.forEach( (person) => {
        pack = {
            "name":person.name,
            "shares": person.shares,
            "gak": person.gak,
            "previousvalue": person.previousvalue
        }
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