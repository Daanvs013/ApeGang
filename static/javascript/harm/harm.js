// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('ticker_price','True')
    socket.emit('table_data_harm','all')
});
//

// intervals
setInterval(function() {
    socket.emit('ticker_price','Harm')
}, 5000); 
//