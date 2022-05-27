export const speedR = document.getElementById("speedRange");
export const cameraR = document.getElementById("cameraRange");
export const steeringR = document.getElementById("steeringRange");
const stop = document.getElementById("stop");
let outSpeed = document.getElementById("outSpeed");
let outCamera = document.getElementById("outCamera");
let outSteering = document.getElementById("outSteering");


//1 --> speed
//2 --> steering
//3 --> camera
export function changeValue_Text(choice, value) {
  switch (choice) {
    case 1:
      // --- SPEED ---
      eel.changeSpeed(speed = speedR.value)
      outSpeed.innerText = speedR.value
      break;
    case 2:
      // --- STEERING ---
      eel.changeSteering(steering = steeringR.value)
      outSteering.innerText = steeringR.value
      break;
    default:
      // --- CAMERA ---
      eel.changeCamera(camera = cameraR.value)
      outCamera.innerText = cameraR.value
      break;
  }
}

function stopEverything() {
  speedR.value = 0;
  steeringR.value = 0;
  cameraR.value = 0;
  changeValue_Text(1, speedR.value)
  changeValue_Text(2, steeringR.value)
  changeValue_Text(3, cameraR.value)
}
speedR.addEventListener("change", () => {
  changeValue_Text(1, speedR.value)
});
cameraR.addEventListener("change", () => {
  changeValue_Text(2, steeringR.value)
});
steeringR.addEventListener("change", () => {
  changeValue_Text(3, cameraR.value)
});

stop.addEventListener("click", () => {
  stopEverything()
})

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
    changeValue_Text(1, speedR.value)
  }
  else if (event.key === 'ArrowDown') {
    speedR.value = speed_val - 1
    changeValue_Text(1, speedR.value)
  }
  else if (event.key === 'ArrowLeft') {
    steeringR.value = steering_val - 1
    changeValue_Text(2, steeringR.value)
  }
  else if (event.key === 'ArrowRight') {
    steeringR.value = steering_val + 1
    changeValue_Text(2, steeringR.value)

  }
  else if (event.code === 'Space') {
    // console.log("ciao")
    // stopEverything()
    steeringR.value = 0
    changeValue_Text(2, steeringR.value)
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
while (true) {
  console.log("-" + gamePad.buttons)
}
console.log("CASDASD  ")
function gameLoop() {
  console.log("asdasdasdasdasd")
  if (!gamepad) {
    return;
  }
  if (gamePad.buttons[0] == 1) {
    console.log("ADADAS")
    changeValue_Text(2, 0) //--> STEERING
    changeValue_Text(1, 0) //--> SPEED
  }

  console.log(gamePad.buttons.axes[2] * 5)

  changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
  changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
  changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA
  start = requestAnimationFrame(gameLoop);
}