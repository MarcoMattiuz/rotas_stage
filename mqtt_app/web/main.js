const speedR = document.getElementById("speedRange");
const cameraR = document.getElementById("cameraRange");
const steeringR = document.getElementById("steeringRange");
const stop = document.getElementById("stop");
let outSpeed = document.getElementById("outSpeed");
let outCamera = document.getElementById("outCamera");
let outSteering = document.getElementById("outSteering");



function stopEverything() {
  speedR.value = 0;
  steeringR.value = 0;
  cameraR.value = 0;
  eel.changeSpeed(speed = speedR.value)
  outSpeed.innerText = speedR.value
  eel.changeSteering(steering = steeringR.value)
  outSteering.innerText = steeringR.value
  eel.changeCamera(camera = cameraR.value)
  outCamera.innerText = cameraR.value
}
speedR.addEventListener("change", () => {
  console.log("ciao")
  eel.changeSpeed(speed = speedR.value)
  outSpeed.innerText = speedR.value
});
cameraR.addEventListener("change", () => {
  eel.changeCamera(camera = cameraR.value)
  outCamera.innerText = cameraR.value
});
steeringR.addEventListener("change", () => {
  eel.changeSteering(steering = steeringR.value)
  outSteering.innerText = steeringR.value
});

// stop.addEventListener("click", () => {
//   stopEverything()
// })

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// comandi da tastiera
document.addEventListener('keydown', (event) => {
  let speed_val = parseInt(speedR.value)
  let steering_val = parseInt(steeringR.value)
  if (event.key === 'ArrowUp' || event.key == 'w') {
    speedR.value = speed_val + 1
    eel.changeSpeed(speed = speedR.value)
    outSpeed.innerText = speedR.value
  }
  else if (event.key === 'ArrowDown' || event.key == 's') {
    speedR.value = speed_val - 1
    eel.changeSpeed(speed = speedR.value)
    outSpeed.innerText = speedR.value
  }
  else if (event.key === 'ArrowLeft' || event.key == 'a') {
    steeringR.value = steering_val - 1
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value
  }
  else if (event.key === 'ArrowRight' || event.key == 'd') {
    steeringR.value = steering_val + 1
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value

  }
  else if (event.code === 'Space') {
    steeringR.value = 0
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value
  } else if (event.key === 'Enter') {
    stopEverything()
  }

  outSpeed.innerText = speedR.value
  outSteering.innerText = steeringR.value
}, false);


var gamePad;
var start;
console.log("ciao")

window.addEventListener("gamepadconnected", function(e) {
  console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
    e.gamepad.index, e.gamepad.id,
    e.gamepad.buttons.length, e.gamepad.axes.length);
    gameLoop();
  });
window.addEventListener("gamepaddisconnected", e => {
  console.log("Gamepad disconnected from index %d: %s",
    e.gamepad.index, e.gamepad.id);
  window.cancelRequestAnimationFrame(start);

});
var interval;

/*if (!('ongamepadconnected' in window)) {
  // No gamepad events available, poll instead.
  interval = setInterval(pollGamepads, 500);
}
function pollGamepads() {
  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads : []);
  for (var i = 0; i < gamepads.length; i++) {
    var gp = gamepads[i];
    if (gp) {
      gamepadInfo.innerHTML = "Gamepad connected at index " + gp.index + ": " + gp.id +
        ". It has " + gp.buttons.length + " buttons and " + gp.axes.length + " axes.";
      gameLoop();
      clearInterval(interval);
    }
  }
}*/

function gameLoop() {
 // console.log(gamePad);
 // console.log("asdasdasdasdasd");

  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  if (!gamepads) {
    return;
  }
  gamePad = gamepads[0];
  //console.log(gamePad);
  //testVibration(gamePad);

  if (gamePad.buttons[0].value==1) {
    console.log(gamePad.buttons[0])
  }
  var valSpeed =Math.round(gamePad.axes[1]*-5);
  if(speedR.value!=valSpeed){
    speedR.value= valSpeed;
    console.log(valSpeed);
    eel.changeSpeed(speed = speedR.value);
  
  }
  var valSterring = Math.round(gamePad.axes[2]*5);
  if(steeringR.value != valSterring){
    steeringR.value = valSterring;
    eel.changeSteering(steering = steeringR.value);
  }




 /* changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
  changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
  changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA*/
  start = window.requestAnimationFrame(gameLoop);

}

function testVibration(gamepad) {
  if (gamepad && gamepad.vibrationActuator) {
    gamepad.vibrationActuator.playEffect("dual-rumble", {
      startDelay: 0,
      duration: 1000,
      weakMagnitude: 1.0,
      strongMagnitude: 1.0,
    });
  }
}
