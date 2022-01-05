// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_daan','all')
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','Daan')
}, 5000); 
//