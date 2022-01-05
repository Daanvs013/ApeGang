// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_index','all')
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','Index')
}, 5000); 
//