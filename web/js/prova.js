/*http://luser.github.io/gamepadtest*/

// Verifica se il browser supporta l'API del gamepad
//var getGamepads = "getGamepads" in navigator ? navigator.getGamepads.bind(navigator) : navigator.webkitGetGamepads.bind(navigator);
//var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);


/*
var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
*/

var on_gp = document.getElementById("on_gp");
var off_gp = document.getElementById("off_gp");

function on(element){
    element.classList.add('on');
    element.classList.remove('off');
}

function off(element){
    element.classList.add('off');
    element.classList.remove('on');
}

function checkControllerStatus() {
    var gamepads=[];

    if (navigator.getGamepads) {
        gamepads = navigator.getGamepads();
    } else if (navigator.webkitGetGamepads) {
        gamepads = navigator.webkitGetGamepads();
    } else if (navigator.mozGetGamepads) {
        gamepads = navigator.mozGetGamepads();
    }

    var controllerConnected = false;
    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];
        if (gamepad) {
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
function value() {
    var gamepads=[];

    if (navigator.getGamepads) {
        gamepads = navigator.getGamepads();
    } else if (navigator.webkitGetGamepads) {
        gamepads = navigator.webkitGetGamepads();
    } else if (navigator.mozGetGamepads) {
        gamepads = navigator.mozGetGamepads();
    }
    for (var i = 0; i < gamepads.length; i++) {
      var gamepad = gamepads[i];
  
      // Controlla se il gamepad è connesso e attivo
      if (gamepad && gamepad.connected && gamepad.buttons.length > 0) {
        let buttons = gamepad.buttons;

        triggerR = triggerRVal(buttons);
        triggerL = triggerLVal(buttons);
  
        if(buttons[5].pressed){
            triggerR=-triggerR;
        }
        if(buttons[4].pressed){
            triggerL=-triggerL;
        }
        controller = JSON.stringify({
            "left": triggerL,
            "right": triggerR
        });
        if (controller === controller_prec) {
        } else {
            controller_prec = controller;
            sendMessage(controller);
        }
  
        if(gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)"){
          if (triggerR > 500 && triggerL > 500) 
          {
            var vibrationPowerR = Math.min((triggerR - 500) / 23, 1);
            var vibrationPowerL = Math.min((triggerL - 500) / 23, 1);
            //lgbt();
            gamepad.vibrationActuator.playEffect("dual-rumble", {
                startDelay: 0,
                duration: 100,
                weakMagnitude: vibrationPowerL,
                strongMagnitude: vibrationPowerR
            });
          }else if(triggerR < -500 && triggerL < -500) {
              var vibrationPowerR = Math.min((-triggerR - 500) / 23, 1);
              var vibrationPowerL = Math.min((-triggerL - 500) / 23, 1);
              
              l//gbt();
              gamepad.vibrationActuator.playEffect("dual-rumble", {
                  startDelay: 0,
                  duration: 100,
                  weakMagnitude: vibrationPowerL,
                  strongMagnitude: vibrationPowerR
              });
          }
          //else{resetColor();}
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
