var websocket;

// connection indicator
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

var camconnect=false;

//check connetion ws
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

        //ip();
        //pos(10, 10, 05);

        on(on_sr);
        off(off_sr);
        
        value(); 
        updateGamepadStatus();
        rqs=true;
    };

    // Messaggio ricevuto dal server
    websocket.onmessage = function (event) {
        receivedMessage = event.data;
        //console.log("ricevuto: "+receivedMessage);
        var json = JSON.parse(receivedMessage);

        if (json.hasOwnProperty("img")) {
            if(!camconnect){
                openCam();
            }
            var src = 'data:image/jpg;base64,' + json.img;
            updateCam(src);
        }

        if (json.hasOwnProperty("latitude")&&json.hasOwnProperty("longitude")&&json.hasOwnProperty("satellites")) {
            pos(json.gps.latitude, json.gps.longitude, json.gps.satellites);
        }

        if (json.hasOwnProperty("level")) {
            updateBattery(Math.abs(json.batt.level) * 100);
        }


        
    }

    // Connessione WebSocket chiusa
    websocket.onclose = function () {
        console.log('WebSocket connection closed');
        on(off_sr);
        off(on_sr);

        reset_battery();
        reset_map();
        reset_cam();

        rqs=false;
    };
}

// lettura ip connesso al ws
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
}