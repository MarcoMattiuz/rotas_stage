
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

stop.addEventListener("click", () => {
  stopEverything()
})
eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}

// comandi da tastiera
document.addEventListener('keydown', (event) => {
  speed_val = parseInt(speedR.value)
  steering_val = parseInt(steeringR.value)

  if (event.key === 'ArrowUp') {
    speedR.value = speed_val + 1
    eel.changeSpeed(speed = speedR.value)
  }
  else if (event.key === 'ArrowDown') {
    speedR.value = speed_val - 1
    eel.changeSpeed(speed = speedR.value)
  }
  else if (event.key === 'ArrowLeft') {
    steeringR.value = steering_val - 1
    eel.changeSteering(steering = steeringR.value)

  }
  else if (event.key === 'ArrowRight') {
    steeringR.value = steering_val + 1
    eel.changeSteering(steering = steeringR.value)

  }
  else if (event.code === 'Space') {
    console.log("ciao")
    stopEverything()
  }

  outSpeed.innerText = speedR.value
  outSteering.innerText = steeringR.value
}, false);