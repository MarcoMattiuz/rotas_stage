var on_sr=document.getElementById("on_sr");
var off_sr=document.getElementById("off_sr");
var gps=document.getElementById("gps");

function on(element){
    element.style.backgroundColor="red";
}
function off(element){
    element.style.backgroundColor="#cccccc";
}

function text(msg){
    gps.innerHTML=msg;
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
    const wsURL = 'ws://rotaspi.local:8000';

    websocket = new WebSocket(wsURL);

    //connessione WebSocket aperta
    websocket.onopen = function() {
        console.log('WebSocket connection opened');
        on(on_sr);
        off(off_sr);
        value(); //funz in controller.js
    }; 

    // Message received from the WebSocket server
    websocket.onmessage = function(event) {
        const message = event.data;
        text("GPS:", message);
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