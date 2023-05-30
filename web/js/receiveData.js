// receiveData.js
var websocket;
var on_sr = document.getElementById("on_sr");
var off_sr = document.getElementById("off_sr");

var connect = false;

function connectPage() {
  if (!connect) {
    connect = !connect;
    connectWebSocket();
  } else {
    connect = !connect;
    websocket.close();
  }
}

function connectWebSocket() {
    
    const wsURL = 'ws://192.168.9.193:8000';

    websocket = new WebSocket(wsURL);
    // Connessione WebSocket aperta
    websocket.onopen = function () {
        console.log('WebSocket connection opened');
        on(on_sr);
        off(off_sr);
        value(); 
        updateGamepadStatus();
        rqs=true;
    };

    // Messaggio ricevuto dal server
    websocket.onmessage = function (event) {
        receivedMessage = event.data;
        //console.log(receivedMessage);
        var json = JSON.parse(receivedMessage);

        pos(json.gps.latitude, json.gps.longitude);
        updateBattery(Math.abs(json.batt.level) * 100);
    }

    // Connessione WebSocket chiusa
    websocket.onclose = function () {
        console.log('WebSocket connection closed');
        on(off_sr);
        off(on_sr);
        reset_battery();
        reset_map();
        rqs=false;
    };
}

