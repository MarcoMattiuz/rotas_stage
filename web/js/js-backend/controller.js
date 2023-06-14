var on_gp=document.getElementsByClassName("on_gp");
var off_gp=document.getElementsByClassName("off_gp");
var controllerSvg = document.getElementsByClassName("controller");

// Funzione per verificare lo stato del controller
function checkControllerStatus() {
    let gamepads = navigator.getGamepads();
    
    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];
        if (gamepad) {
            controllerConnect = true;
            break;
        }else{
            controllerConnect = false;
        }
    }
 
    if (controllerConnect) {
        on(on_gp);
        off(off_gp);
        remove_d_none(controllerSvg[0])
        closeJoy();
        closeMic();

        if(manager){
            document.getElementById('joystick').style.display = 'none';
            manager.destroy();
            manager = null;
            destroyDivJoystick();
        }

    } else {

        off(on_gp);
        on(off_gp);
        resetColor();
        add_d_none(controllerSvg[0]);
        if(connect){
            openJoy();
            openMic();
        }
    }

    checkNavPad();
}
setInterval(checkControllerStatus, 50);

var gamepad;
var controller_prec="";
var controller="";
var triggerR;
var triggerL;

function value() {
    let gamepads = navigator.getGamepads();

    for (var i = 0; i < gamepads.length; i++) {
        gamepad= gamepads[i];

    if (gamepad&&connect)  {

            let buttons = gamepad.buttons;
            let axes = gamepad.axes;

            if(buttons[0].pressed){
                cingolato(buttons);
                vibration();
                 
            }else if(buttons[1].pressed){
                if(!rec){
                    rec=true;
                    openMic();
                    openRec();
                    voice_commands();
                    recognition.start();
                }
            }else{
                controller=JSON.stringify({"left": 0,"right": 0,});
                stearing(axes);
            }    
            
            if (controller === controller_prec) {
            } else {
                controller_prec = controller;
                sendMessage(controller);
            }     
        }
    }

    setTimeout(value, 0.05)
}

function cingolato(buttons){
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
        "right": triggerR,
    });

}

function vibration(){
    if(gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)"){
        if (triggerR > 500 && triggerL > 500) 
        {
            var vibrationPowerR = Math.min((triggerR - 500) / 23, 1);
            var vibrationPowerL = Math.min((triggerL - 500) / 23, 1);
            lgbt();
            gamepad.vibrationActuator.playEffect("dual-rumble", {
                startDelay: 0,
                duration: 100,
                weakMagnitude: vibrationPowerL,
                strongMagnitude: vibrationPowerR
            });
        } 
        else if(triggerR < -500 && triggerL < -500) 
            {
                var vibrationPowerR = Math.min((-triggerR - 500) / 23, 1);
                var vibrationPowerL = Math.min((-triggerL - 500) / 23, 1);
                
                lgbt();
                gamepad.vibrationActuator.playEffect("dual-rumble", {
                    startDelay: 0,
                    duration: 100,
                    weakMagnitude: vibrationPowerL,
                    strongMagnitude: vibrationPowerR
                });
            }
            else{resetColor();}
    }
}

var stearing_prec="";
var stearing_val="";

function stearing(axes){
    var x=axes[0];
    var y=axes[1];

    if(x>=-0.05&&x<=0.05){
        x=0;
    }
    if(y>=-0.05&&y<=0.05){
        y=0;
    }

    var accel = Math.round(y* 1023);
    var steer = Math.round(x* 1023);

    stearing_val = JSON.stringify({
        "accel": -accel,
        "steer": steer,
    });

    if (stearing_val === stearing_prec) {
    } else {
        stearing_prec = stearing_val;
        sendMessage(stearing_val);
    }
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

function getVal(){
    return triggerRVal(buttons);
}