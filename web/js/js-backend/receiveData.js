// connection indicator
var on_sr=document.getElementsByClassName("on_sr");
var off_sr=document.getElementsByClassName("off_sr");

function on(element){
    for (let i = 0; i < element.length; i++) {
        element[i].classList.add('on');
        element[i].classList.remove('off');
    }
}

function off(element){
    for (let i = 0; i < element.length; i++) {
        element[i].classList.add('off');
        element[i].classList.remove('on');
    }
}


//check connetion ws
function connectPage() {
  if (!connect) {
    connect = true;
    connectWebSocket();
    
    loading_cam.classList.remove("d-none");
    loading_map.classList.remove("d-none");

  }else {
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

        //ip();
        //pos(10, 10, 05);
        
        on(on_sr);
        off(off_sr);
        
        value(); 
        updateGamepadStatus();

        checkNavServer();
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
        }else{
            reset_cam();
        }

        if (json.hasOwnProperty("dets")){
            if(camconnect){
                
                read_dets(json.dets);
            }
        }else{
            var json_null=null;
            read_dets(json_null);
        }

        if (json.hasOwnProperty("gps")) {
            pos(json.gps.latitude, json.gps.longitude, json.gps.satellites);
            //pos(10, 10, 05);
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

    on(off_sr);
    off(on_sr);

    reset_battery();
    reset_map();
    reset_cam();

    loading_cam.classList.add("d-none");
    loading_map.classList.add("d-none");

    checkNavServer();
    resetColor();

    if(manager){
        destroyJoystick();
        destroyDivJoystick();
    }

    rqs=false;
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

