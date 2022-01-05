// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_wenting','all')
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','Wenting')
}, 5000); 
//