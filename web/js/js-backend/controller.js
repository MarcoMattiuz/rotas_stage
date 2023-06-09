var on_gp=document.getElementsByClassName("on_gp");
var off_gp=document.getElementsByClassName("off_gp");
var controllerSvg = document.getElementsByClassName("controller");

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
        
        controllerSvg[0].classList.remove("d-none");

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
        
        controllerSvg[0].classList.add("d-none");
    }

    checkNavPad();
}
setInterval(checkControllerStatus, 50);

var gamepad;

var controller_prec="";
var controller="";

/*
const data = new Date()
var prevTime = data.getTime();
var prevR=0, prevL=0;*/

var triggerR;
var triggerL;

//___CONTROLLER___
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

    //console.log("d L:"+derivata(triggerL,prevL)+" d R:"+derivata(triggerR,prevR));
    /*prevL=triggerL;
    prevR=triggerR;
    const data=new Date();
    dL=derivata(triggerL,prevL);
    dR=derivata(triggerR,prevR);
    prevTime = data.getTime();
    */

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