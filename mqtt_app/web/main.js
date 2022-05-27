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
    changeValue_Text(2, 0) //--> STEERING
    changeValue_Text(1, 0) //--> SPEED
  }

  if(gamePad.axes[2]>0.5){
    console.log(gamePad.axes[2]);
  }
  if(gamePad.axes[3]>-0.5){
    console.log("3",
    gamePad.axes[3]);
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
