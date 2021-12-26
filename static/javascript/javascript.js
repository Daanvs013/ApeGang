//round function
function round(number, d) {
  return Number(Math.round(number+'e'+d)+'e-'+d);
}
//

// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
});


//ticker_price
socket.on('ticker_price_response', function(data){
    //console.log(data)
    var id = document.getElementById("ticker_price");
    id.innerHTML = data
});
//

//table_data
socket.on('table_data_response', function(data){
    //console.log(data)
    var table = document.getElementById("table");
    var price = document.getElementById("ticker_price").innerHTML;
    if (price=='prijs ophalen...'){
        
    } else {
        data.forEach( (person) => {
            row = 0
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
            } 
            value = round(price*person.shares,2)
            cost = round(person.shares*person.gak,2);
            table.rows[row].cells[1].innerHTML = value;
            profit = round(value - cost,2);
            rendement = round(100*profit/cost,2)
            table.rows[row].cells[4].innerHTML = profit;
            table.rows[row].cells[5].innerHTML = rendement
            table.rows[row].cells[6].innerHTML = person.shares;
            table.rows[row].cells[7].innerHTML = person.gak;
            table.rows[row].cells[8].innerHTML = cost;
        });
    }
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data','True')
}, 2000); 
//