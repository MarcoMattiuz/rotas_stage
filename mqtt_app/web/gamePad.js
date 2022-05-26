

var gamePad;
var start;
window.addEventListener("gamepadconnected", e =>{

    console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
    e.gamepad.index, e.gamepad.id,
    e.gamepad.buttons.length, e.gamepad.axes.length);
    gamePad = navigator.getGamepads()[e.gamepad.index]
});
window.addEventListener("gamepaddisconnected", e =>{
    console.log("Gamepad disconnected from index %d: %s",
    e.gamepad.index, e.gamepad.id);
    cancelRequestAnimationFrame(start);
    gamePad = null;
});

function gameLoop(){
    
    if (!gamepad) {
      return;
    }
    if(gamePad.buttons[0]==1){
        eel.changeSteering(steering = 0);
        eel.changeSpeed(speed = 0);
       
    }
    eel.changeSteering(steering = gamePad.buttons.axes[2]*5);
    eel.changeSpeed(speed = gamePad.buttons.axes[3]*5);
    eel.changeCamera(camera = gamePad.buttons.axes[0]*5)
    start = requestAnimationFrame(gameLoop);
}
