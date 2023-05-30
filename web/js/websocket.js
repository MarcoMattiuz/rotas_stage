
var on_sr=document.getElementById("on_sr");
var off_sr=document.getElementById("off_sr");
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
        updateGamepadStatus();
        
    }; 

    //mesaggio ricevuto dal server
    websocket.onmessage = function(event) {
        receivedMessage = event.data;
        console.log(receivedMessage);
        var json = JSON.parse(receivedMessage);
    

        pos(json.gps.latitude,json.gps.longitude);
        //console.log(Math.abs(json.batt.level));
        updateBattery(Math.abs(json.batt.level)*100);
        //console.log("lat: "+json.gps.latitude+" long: "+json.gps.longitude+" batt: " +json.batt.volts);
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
        console.log(message);
        websocket.send(message);
    }
}