//init socket
var socket = io.connect()

socket.on('client_connect_response', function(data){
    console.log(`ID: ${data}`)
});
//
