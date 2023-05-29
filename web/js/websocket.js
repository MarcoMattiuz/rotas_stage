var on_sr=document.getElementById("on_sr");
var off_sr=document.getElementById("off_sr");
var gps=document.getElementById("gps");

function on(element){
    element.style.backgroundColor="red";
}
function off(element){
    element.style.backgroundColor="#cccccc";
}


var connect=false;
function connectPage(){
    if(!connect){
        connect=!connect;
        connectWebSocket();
    }else{
        connect=!connect;
        websocket.close();
    }
}

function connectWebSocket() {
    const wsURL = 'ws://192.168.9.193:8000';

    websocket = new WebSocket(wsURL);

    //connessione WebSocket aperta
    websocket.onopen = function() {
        console.log('WebSocket connection opened');
        on(on_sr);
        off(off_sr);
        value(); //funz in controller.js
    }; 

    //mesaggio ricevuto dal server
    websocket.onmessage = function(event) {
        receivedMessage = event.data;
        var jsonpos = JSON.parse(receivedMessage); 
        pos(jsonpos.latitude,jsonpos.longitude);
    };

    //connessione WebSocket chiusa
    websocket.onclose = function() {
        console.log('WebSocket connection closed');
        on(off_sr);
        off(on_sr);
    };
}

function sendMessage(message) {
    // msg inviare al WebSocket
    if(message!=undefined){
        websocket.send(message);
    }
}