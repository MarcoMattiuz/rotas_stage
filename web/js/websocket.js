let websocket;

function connectWebSocket() {
    const wsURL = 'ws://rotaspi.local:8000';

    websocket = new WebSocket(wsURL);

    //connessione WebSocket aperta
    websocket.onopen = function() {
        console.log('WebSocket connection opened');
    };

    //messaggio ricevuto dal server WebSocket
    websocket.onmessage = function(event) {
        const message = event.data;
        console.log('Messaggio ricevuto:', message);
    };

    //connessione WebSocket chiusa
    websocket.onclose = function() {
        console.log('WebSocket connection closed');
    };
}

function sendMessage(message) {
    // msg inviare al WebSocket
    if(message!=undefined){
        websocket.send(message);
    }
}

var controller_prec="";
var controller="";

//___CONTROLLER___
function value() {
    let gamepads = navigator.getGamepads();

    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];

        if (gamepad && gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)") {
            let buttons = gamepad.buttons;
            let axes = gamepad.axes;

            controller = JSON.stringify({

                triggerR: triggerR(buttons),
                triggerL: triggerL(buttons),
                
                buttonR: buttons[5].pressed,
                buttonL: buttons[4].pressed,
                
                axesXR: axes[0],
                axesYR: axes[1],
                axesXL: axes[2],
                axesYL: axes[3]

            });
            
            if(controller===controller_prec){
                console.log("prova");
            }else{
                controller_prec=controller;
                console.log("prova");
                sendMessage(controller);
            }
            
        }        
    }
    
    requestAnimationFrame(value);
}

function triggerR(buttons){
    if (buttons[7].pressed) {
        var val = buttons[7].value - 0.09
        if (val < 0) val = 0; 
        var ris=(val*1023)/0.91;

        return Math.floor(ris);
    }else{
        return 0;
    }
}

function triggerL(buttons){
    if (buttons[6].pressed) {
        var val = buttons[6].value - 0.09
        if (val < 0) val = 0; 
        var ris=(val*1023)/0.91;

        return Math.floor(ris);
    }else{
        return 0;
    }
}