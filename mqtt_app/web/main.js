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
  changeValue_Text(2, steeringR.value)
  changeValue_Text(3, cameraR.value)
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

  if (event.key === 'ArrowUp') {
    speedR.value = speed_val + 1
    eel.changeSpeed(speed = speedR.value)
    outSpeed.innerText = speedR.value
  }
  else if (event.key === 'ArrowDown') {
    speedR.value = speed_val - 1
    eel.changeSpeed(speed = speedR.value)
    outSpeed.innerText = speedR.value
  }
  else if (event.key === 'ArrowLeft') {
    steeringR.value = steering_val - 1
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value
  }
  else if (event.key === 'ArrowRight') {
    steeringR.value = steering_val + 1
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value

  }
  else if (event.code === 'Space') {
    // console.log("ciao")
    // stopEverything()
    steeringR.value = 0
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value
  }

  outSpeed.innerText = speedR.value
  outSteering.innerText = steeringR.value
}, false);


var gamePad;
var start;
console.log("ciao")
window.addEventListener("gamepadconnected", e => {

  console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
    e.gamepad.index, e.gamepad.id,
    e.gamepad.buttons.length, e.gamepad.axes.length);
  gamePad = navigator.getGamepads()[e.gamepad.index]
});
window.addEventListener("gamepaddisconnected", e => {
  console.log("Gamepad disconnected from index %d: %s",
    e.gamepad.index, e.gamepad.id);
  cancelRequestAnimationFrame(start);
  gamePad = null;
});

function gameLoop() {
  if (!gamepad) {
    return;
  }
  if (gamePad.buttons[0] == 1) {
    speedR.value = 0;
    steeringR.value = 0;
    eel.changeSteering(steering = steeringR.value)
    outSteering.innerText = steeringR.value
    eel.changeSpeed(speed = speedR.value)
    outSpeed.innerText = speedR.value
  }

  console.log(gamePad.buttons.axes[2] * 5)

  speedR.value = gamePad.buttons.axes[3] * 5;
  steeringR.value = gamePad.buttons.axes[2] * 5;
  cameraR.value = gamePad.buttons.axes[0] * 5;
  eel.changeSteering(steering = steeringR.value)
  outSteering.innerText = steeringR.value
  eel.changeSpeed(speed = speedR.value)
  outSpeed.innerText = speedR.value
  eel.changeSteering(steering = steeringR.value)
  outSteering.innerText = steeringR.value

  start = requestAnimationFrame(gameLoop);
}