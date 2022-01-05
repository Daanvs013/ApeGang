//realtime table
socket.on('ticker_price_response', function(data){
    //console.log(data)
    var table = document.getElementById('table');

    //ticker div
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


    //table
    if(table_list == []){
        
    } else {
        for (i = table.rows.length ; i > 1; i--){
            table.deleteRow(i-1)
        } 
        table_list.forEach((td) => {
            //add new row
            var row = table.insertRow(-1);
            //insert name
            var cell0 =  row.insertCell(0)
            cell0.innerHTML = td.name;
            //insert value
            value = td.shares*price;
            var cell1 = row.insertCell(1)
            cell1.innerHTML = round(value,2);
            //insert daily change and relchange
            change = value - td.previousvalue;
            var cell2 = row.insertCell(2)
            cell2.innerHTML = round(change,2);
            relchange=0
            if(td.previousvalue>0){
                relchange = 100*(change/td.previousvalue);
            }
            var cell3 = row.insertCell(3)
            cell3.innerHTML = round(relchange,2);
            //cost
            cost = td.shares*td.gak
            //profit
            profit = value-cost
            var cell4 = row.insertCell(4)
            cell4.innerHTML = round(profit,2);
            rendement = 0
            if(cost>0){
                rendement = 100*profit/cost
            }
            var cell5 = row.insertCell(5)
            cell5.innerHTML = round(rendement,2);
            //number of shares
            row.insertCell(6).innerHTML = td.shares;
            //gak
            row.insertCell(7).innerHTML = td.gak;
            //cost
            row.insertCell(8).innerHTML = round(cost,2);


            //colors
            if(change<0){
                cell2.style.color = 'red'
                cell3.style.color = 'red'
            } else {
                cell2.style.color = '#009879';
                cell3.style.color = '#009879';
            }
            if(profit<0){
                cell4.style.color = 'red'
                cell5.style.color = 'red'
            } else {
                cell4.style.color = '#009879';
                cell5.style.color = '#009879';
            }
        });
    }
    
});
//

//table_data
table_list = []
socket.on('table_data_response', function(data){
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
    console.log(table_list)
});
//