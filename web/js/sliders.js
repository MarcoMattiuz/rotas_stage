var speedRange = document.getElementById("speedRange");
var steeringRange = document.getElementById("steeringRange");
var cameraRange = document.getElementById("cameraRange");
var mSpeed = document.getElementById("mSpeed");
var pSpeed = document.getElementById("pSpeed");
var mSteering = document.getElementById("mSteering");
var pSteering = document.getElementById("pSteering");
var mCamera = document.getElementById("mCamera");
var pCamera = document.getElementById("pCamera");

mSpeed.addEventListener("click", function () {
    speedRange.stepDown();
}, false);

pSpeed.addEventListener("click", function () {
    speedRange.stepUp();
}, false);


mSteering.addEventListener("click", function () {
    steeringRange.stepDown();
}, false);

pSteering.addEventListener("click", function () {
    steeringRange.stepUp();
}, false);


mCamera.addEventListener("click", function () {
    cameraRange.stepDown();
}, false);

pCamera.addEventListener("click", function () {
    cameraRange.stepUp();
}, false);