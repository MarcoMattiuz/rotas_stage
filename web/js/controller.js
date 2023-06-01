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

// Funzione per verificare lo stato del controller
function checkControllerStatus() {
    let gamepads = navigator.getGamepads();
    
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
const data = new Date()
var prevTime = data.getTime();
var prevR=0, prevL=0;


var triggerR;
var triggerL;

//___CONTROLLER___
function value() {
    let gamepads = navigator.getGamepads();

    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];

    if (gamepad)  {

            let buttons = gamepad.buttons;
            let axes = gamepad.axes;

            triggerR = triggerRVal(buttons);
            triggerL = triggerLVal(buttons);
    
            if(buttons[5].pressed){
                triggerR=-triggerR;
            }
            if(buttons[4].pressed){
                triggerL=-triggerL;
            }

            //console.log("d L:"+derivata(triggerL,prevL)+" d R:"+derivata(triggerR,prevR));
            /*prevL=triggerL;
            prevR=triggerR;
            const data=new Date();
            dL=derivata(triggerL,prevL);
            dR=derivata(triggerR,prevR);*/

            prevTime = data.getTime();
            controller = JSON.stringify({
                "left": triggerL,
                "right": triggerR,

                /*buttonR: buttons[5].value,
                buttonL: buttons[4].value,

                axesXR:axesVal(axes[2]),
                axesYR:axesVal(axes[3]),
                axesXL:axesVal(axes[0]),
                axesYL:axesVal(axes[1])*/

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

function derivata(val, prev){
    const d = new Date();
    dTime = d.getTime() - prevTime;
    dVal = val - prev;

    return dVal/dTime;
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