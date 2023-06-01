// sendData.js
var websocket;

function sendMessage(message) {
    // msg inviare al WebSocket
    if (message != undefined) {
        websocket.send(message);
    }
}

var rqs=false;
function request(){
    if(rqs)
    var data = JSON.stringify({
        "gps": null,
        "batt": null
    });
    sendMessage(data);
}

//setInterval(request, 3000);