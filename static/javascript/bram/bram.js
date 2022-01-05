// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_bram','all')
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','Bram')
}, 5000); 
//