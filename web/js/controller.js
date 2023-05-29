var on_gp = document.getElementById("on_gp");
var off_gp = document.getElementById("off_gp");

function on(element) {
  element.style.backgroundColor = "red";
}

function off(element) {
  element.style.backgroundColor = "#cccccc";
}
// Funzione per verificare lo stato del controller
function checkControllerStatus() {
  let gamepads = navigator.getGamepads();

  // Verifica se il controller è collegato
  var controllerConnected = false;
  for (var i = 0; i < gamepads.length; i++) {
    let gamepad = gamepads[i];
    if (gamepad && (gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)" || gamepad.id === "Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)")) {
        controllerConnected = true;
      break;
    }
  }

  if (controllerConnected) {
    on(on_gp);
    off(off_gp);
  } else {
    off(on_gp);
    on(off_gp);
  }
}
setInterval(checkControllerStatus, 10);

var controller_prec="";
var controller="";
//___CONTROLLER___
function value() {
    let gamepads = navigator.getGamepads();

    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];

    if (gamepad && (gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)" || gamepad.id === "Xbox Wireless Controller (STANDARD GAMEPAD Vendor: 045e Product: 0b13)" || gamepad.id === "")) {
            
            let buttons = gamepad.buttons;
            let axes = gamepad.axes;

            var triggerR = triggerRVal(buttons);
            var triggerL = triggerLVal(buttons);

            controller = JSON.stringify({
                triggerR: triggerR,
                triggerL: triggerL,

                buttonR: buttons[5].value,
                buttonL: buttons[4].value,

                axesXR:axesVal(axes[2]),
                axesYR:axesVal(axes[3]),
                axesXL:axesVal(axes[0]),
                axesYL:axesVal(axes[1])
            });

            if (controller === controller_prec) {
                
            } else {
                controller_prec = controller;
                sendMessage(controller); //funz in websocket.js
            }

            
            if(gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)"){
                if (triggerR > 500 && triggerL > 500) {
                    var vibrationPowerR = Math.min((triggerR - 500) / 23, 1);
                    var vibrationPowerL = Math.min((triggerL - 500) / 23, 1);

                    gamepad.vibrationActuator.playEffect("dual-rumble", {
                        startDelay: 0,
                        duration: 100,
                        weakMagnitude: vibrationPowerL,
                        strongMagnitude: vibrationPowerR
                    });
                }
            }

            
        }
    }

    setTimeout(value, 0.01)
}


function triggerRVal(buttons){
    if (buttons[7].pressed) {
        var val = buttons[7].value - 0.09
        if (val < 0) val = 0; 
        var ris=(val*1023)/0.91;

        return Math.floor(ris);
    }else{
        return 0;
    }
}

function triggerLVal(buttons){
    if (buttons[6].pressed) {
        var val = buttons[6].value - 0.09
        if (val < 0) val = 0; 
        var ris=(val*1023)/0.91;

        return Math.floor(ris);
    }else{
        return 0;
    }
}

function axesVal(val){
    if (val>-0.05&&val<0.05) {
        val = 0;
    }else{
        val = Math.floor(val*1023);
    }
    return val;
}
