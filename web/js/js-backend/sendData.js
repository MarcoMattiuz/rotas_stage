var websocket;

// invio msg al server.py
function sendMessage(message) {
    if (message != undefined) {
        websocket.send(message);
    }
}

var rqs=false;
//richiesta info 
function request(){
    if(rqs)
    var data = JSON.stringify({
        "gps": null,
        "batt": null
    });
    sendMessage(data);
}

setInterval(request, 3000);