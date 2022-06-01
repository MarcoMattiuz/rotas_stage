var speedRange = document.getElementById("speedRange");
var steeringRange = document.getElementById("steeringRange");
var cameraRange = document.getElementById("cameraRange");
var mSpeed = document.getElementById("mSpeed");
var pSpeed = document.getElementById("pSpeed");
var mSteering = document.getElementById("mSteering");
var pSteering = document.getElementById("pSteering");
var mCamera = document.getElementById("mCamera");
var pCamera = document.getElementById("pCamera");
// let outSpeed = document.getElementById("outSpeed");
// let outCamera = document.getElementById("outCamera");
// let outSteering = document.getElementById("outSteering");

mSpeed.addEventListener("click", function () {
    speedRange.value -= 1;
    outSpeed.innerText = speedRange.value
}, false);

pSpeed.addEventListener("click", function () {
    speedRange.value += 1;
    outSpeed.innerText = speedRange.value
}, false);


mSteering.addEventListener("click", function () {
    steeringRange.value -= 1;
    outSteering.innerText = steeringRange.value
}, false);

pSteering.addEventListener("click", function () {
    steeringRange.value += 1;
    outSteering.innerText = steeringRange.value
}, false);


mCamera.addEventListener("click", function () {
    cameraRange.value -= 1;
    outCamera.innerText = cameraRange.value
}, false);

pCamera.addEventListener("click", function () {
    cameraRange.value += 1;
    outCamera.innerText = cameraRange.value
}, false);