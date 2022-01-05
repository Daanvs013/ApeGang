// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('history_table',["Daan","Degiro",5])
});
//