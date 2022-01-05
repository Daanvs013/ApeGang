//init socket
var socket = io.connect()

socket.on('client_connect_response', function(data){
    console.log(`SID: ${data}`)
    document.getElementById('sid').innerHTML = `SID: ${data}`;
    sessionStorage.setItem("sid",data);
});
//

//round function
function round(number, d) {
  return Number(Math.round(number+'e'+d)+'e-'+d);
}
//

//backdoor
function backdoor(input){
  socket.emit("console",input)
}
socket.on("console_response", function(data){
  console.log(data)
})
//