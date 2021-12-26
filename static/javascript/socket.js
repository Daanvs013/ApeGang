//init socket
var socket = io.connect('localhost:5000')

socket.on('client_connect_response', function(data){
    console.log(`ID: ${data}`)
});
//