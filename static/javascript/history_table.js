//realtime table
socket.on('history_table_response', function(data){
    console.log(data)
    var table = document.getElementById('table_history');

    //table
    data.forEach((td) => {
        //add new row
        var row = table.insertRow(-1);
        //insert day
        day = td.day.split(" ")
        var cell0 =  row.insertCell(0)
        cell0.innerHTML = day[0];
        //insert value
        var cell1 = row.insertCell(1)
        cell1.innerHTML = round(td.value,2);
        //insert change
        var cell2 = row.insertCell(2)
        cell2.innerHTML = round(td.change,2);
        //insert relchange
        var cell3 = row.insertCell(3)
        cell3.innerHTML = round(td.relchange,2);
        //profit
        var cell4 = row.insertCell(4)
        cell4.innerHTML = round(td.profit,2);
        //rendement
        var cell5 = row.insertCell(5)
        cell5.innerHTML = round(td.rendement,2);
        //number of shares
        row.insertCell(6).innerHTML = td.shares;
        //gak
        row.insertCell(7).innerHTML = round(td.gak,2);
        //cost
        cost = td.shares * td.gak
        row.insertCell(8).innerHTML = round(cost,2)


        //colors
        if(td.change<0){
            cell2.style.color = 'red'
            cell3.style.color = 'red'
        } else {
            cell2.style.color = '#009879';
            cell3.style.color = '#009879';
        }
        if(td.profit<0){
            cell4.style.color = 'red'
            cell5.style.color = 'red'
        } else {
            cell4.style.color = '#009879';
            cell5.style.color = '#009879';
        }
    }); 
});
//