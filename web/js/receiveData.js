
var websocket;
var on_sr=document.getElementById("on_sr");
var off_sr=document.getElementById("off_sr");

function on(element){
    element.classList.add('on');
    element.classList.remove('off');
}

function off(element){
    element.classList.add('off');
    element.classList.remove('on');
}

var connect = false;

function connectPage() {
  if (!connect) {
    connect = true;
    connectWebSocket();
  } else {
    connect = false;
    websocket.close();
    on(off_sr);
    off(on_sr);

    reset_battery();
    reset_map();
    rqs=false;

  }
}

function connectWebSocket() {
    
    const wsURL = 'wss://wsstage.rotas.eu';

    websocket = new WebSocket(wsURL);
    // Connessione WebSocket aperta
    websocket.onopen = function () {
        console.log('WebSocket connection opened');

        fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            const ip = data.ip;
            sendMessage(JSON.stringify({"msg": ip}));
        })
        .catch(error => {
            console.error('Error retrieving IP address:', error);
            sendMessage(JSON.stringify({"msg": "Ip error"}));
        });
        
        on(on_sr);
        off(off_sr);
        value(); 
        updateGamepadStatus();
        rqs=true;
    };

    // Messaggio ricevuto dal server
    websocket.onmessage = function (event) {
        receivedMessage = event.data;
        console.log("ricevuto: "+receivedMessage);
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

