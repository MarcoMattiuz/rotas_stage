
const speedR = document.getElementById("speedRange");
const cameraR = document.getElementById("cameraRange");
const rotationR = document.getElementById("rotationRange");

speedR.addEventListener("change", () => { eel.changeSpeed(speed = speedR.value) });
cameraR.addEventListener("change", () => { eel.changeCamera(camera = cameraR.value) });
rotationR.addEventListener("change", () => { eel.changeRotation(rotation = rotationR.value) });


eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}