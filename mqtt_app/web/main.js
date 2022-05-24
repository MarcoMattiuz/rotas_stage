
const speedR = document.getElementById("speedRange");
const cameraR = document.getElementById("cameraRange");
const steeringR = document.getElementById("steeringRange");

speedR.addEventListener("change", () => { eel.changeSpeed(speed = speedR.value) });
cameraR.addEventListener("change", () => { eel.changeCamera(camera = cameraR.value) });
steeringR.addEventListener("change", () => { eel.changeSteering(steering = steeringR.value) });


eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}