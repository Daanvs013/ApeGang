// when document is loaded, ask for data
$( document ).ready(function() {
    socket.emit('history_table',["Harm","Totaal",5])
});
//