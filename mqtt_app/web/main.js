
const speedR = document.getElementById("speedRange");
const cameraR = document.getElementById("cameraRange");
const steeringR = document.getElementById("steeringRange");

let outSpeed = document.getElementById("outSpeed");
let outCamera = document.getElementById("outCamera");
let outSteering = document.getElementById("outSteering");

speedR.addEventListener("change", () => { eel.changeSpeed(speed = speedR.value) });
cameraR.addEventListener("change", () => { eel.changeCamera(camera = cameraR.value) });
steeringR.addEventListener("change", () => { eel.changeSteering(steering = steeringR.value) });


speedR.addEventListener("change", () => {
  outSpeed.innerText = speedR.value
})
cameraR.addEventListener("change", () => {
  outCamera.innerText = cameraR.value
})
steeringR.addEventListener("change", () => {
  outSteering.innerText = steeringR.value
})
eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}