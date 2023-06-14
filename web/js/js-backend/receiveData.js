var on_sr=document.getElementsByClassName("on_sr");
var off_sr=document.getElementsByClassName("off_sr");

function connectPage() {
  if (!connect) {

    connect = true;
    connectWebSocket();
  }else {

    sendMessage(JSON.stringify({"sound":"disconnesso"}));
    websocket.close();
    reset_all();
    
  }
}

function connectWebSocket() {
    
    const wsURL = 'wss://wsstage.rotas.eu';
    websocket = new WebSocket(wsURL);
    // Connessione WebSocket aperta

    websocket.onopen = function () {
        console.log('WebSocket connection opened');

        on(on_sr);
        off(off_sr);
        remove_d_none(document.getElementById("loading_cam"));
        remove_d_none(document.getElementById("loading_map"));
        openJoy();
        openMic();
        checkNavServer();
        
        updateGamepadStatus();
        value();
        rqs=true;
        
        sendMessage(JSON.stringify({"sound":"connesso"}));
    };

    // Messaggio ricevuto dal server
    websocket.onmessage = function (event) {
        receivedMessage = event.data;
        console.log("ricevuto: "+receivedMessage);
        var json = JSON.parse(receivedMessage);

        if (json.hasOwnProperty("img")) {
            if(!camconnect){
                openCam();
            } 
            var src = 'data:image/jpg;base64,' + json.img;
            updateCam(src);    
        }else{
            reset_cam();
        }

        if (json.hasOwnProperty("dets")){
            if(camconnect){
                read_dets(json.dets);
                drawRectangle(10,10,100,100);
            }
        }else{
            read_dets(null);
        }

        if (json.hasOwnProperty("gps")) {
            pos(json.gps.longitude, json.gps.latitude, json.gps.satellites);
        }

        if (json.hasOwnProperty("batt")) {
            updateBattery(Math.abs(json.batt.level) * 100);
        }
    }

    // Connessione WebSocket chiusa
    websocket.onclose = function () {
        console.log('WebSocket connection closed');
        reset_all();
    
    };
}

function reset_all(){
    connect=false;

    off(on_sr);
    on(off_sr);

    add_d_none(document.getElementById("loading_cam"));
    add_d_none(document.getElementById("loading_map"));

    closeJoy();
    closeMic();
    checkNavServer();
    resetColor();

    reset_battery();
    reset_map();
    reset_cam();

    if(manager){
        destroyJoystick();
        destroyDivJoystick();
    }

    rqs=false;
}

// lettura ip connesso al ws
/*
function ip(){
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        const ip = data.ip;
        sendMessage(JSON.stringify({"ip": ip}));
    })
    .catch(error => {
        console.error('Error retrieving IP address:', error);
        sendMessage(JSON.stringify({"ip": "Ip error"}));
    });
}*/

