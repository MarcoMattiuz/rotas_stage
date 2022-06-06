const speedR = document.getElementById("speedRange"); //
const cameraR = document.getElementById("cameraRange"); //
const steeringR = document.getElementById("steeringRange"); //
const stopAll = document.getElementById("stopAll");
const stopSteering = document.getElementById("stopSteering");
const resetCamera = document.getElementById("resetCamera")
let outSpeed = document.getElementById("outSpeed");
let outCamera = document.getElementById("outCamera");
let outSteering = document.getElementById("outSteering");
let on_sr = document.getElementById("on_sr");
let off_sr = document.getElementById("off_sr");
let on_gp = document.getElementById("on_gp");
let off_gp = document.getElementById("off_gp");
var mSpeed = document.getElementById("mSpeed");
var pSpeed = document.getElementById("pSpeed");
var mSteering = document.getElementById("mSteering");
var pSteering = document.getElementById("pSteering");
var mCamera = document.getElementById("mCamera");
var pCamera = document.getElementById("pCamera");

function gpON() {
  on_gp.style.background = "#33a532"
  on_gp.style.boxShadow = "0 0 15px #33a532"
  off_gp.style.background = "#cccccc"
  off_gp.style.boxShadow = "none"
}
function gpOFF() {
  off_gp.style.background = "#bb1e10"
  off_gp.style.boxShadow = "0 0 15px  #bb1e10"
  on_gp.style.background = "#cccccc"
  on_gp.style.boxShadow = "none"
}
function srON() {
  on_sr.style.background = "#33a532"
  on_sr.style.boxShadow = "0 0 15px #33a532"
  off_sr.style.background = "#cccccc"
  off_sr.style.boxShadow = "none"
}
function srOFF() {
  off_sr.style.background = "#bb1e10"
  off_sr.style.boxShadow = "0 0 15px  #bb1e10"
  on_sr.style.background = "#cccccc"
  on_sr.style.boxShadow = "none"
}
function stopEverything() {
  speedR.value = 0;
  steeringR.value = 0;
  cameraR.value = 0;
  ws.send("speed:0" + 0);
  outSpeed.innerText = speedR.value
  ws.send("steering:0" + 0);
  outSteering.innerText = steeringR.value
  ws.send("camera:0" + 0);
  outCamera.innerText = cameraR.value
}


/* *************** */
gpOFF()
srOFF()
const ws = new WebSocket("ws://192.168.8.40:8000");
ws.addEventListener("open", () => {
  console.log("we are connected");
  srON()
  speedR.addEventListener("change", () => {
    ws.send("speed:0" + speedR.value);
    outSpeed.innerText = speedR.value;
  });
  cameraR.addEventListener("change", () => {
    ws.send("camera:0" + cameraR.value);
    outCamera.innerText = cameraR.value;
  });
  steeringR.addEventListener("change", () => {
    ws.send("steering:0" + steeringR.value);
    outSteering.innerText = steeringR.value;
  });

  stopAll.addEventListener("click", () => {
    stopEverything()
  })
  stopSteering.addEventListener("click", () => {
    steeringR.value = 0
    outSteering.innerText = steeringR.value
    ws.send("steering:0" + steeringR.value);
  })
  resetCamera.addEventListener("click", () => {
    cameraR.value = 0;
    outCamera.innerText = cameraR.value
    ws.send("camera:0" + cameraR.value);
  })


  document.addEventListener('keydown', (event) => {
    let speed_val = parseInt(speedR.value)
    let steering_val = parseInt(steeringR.value)

    if (event.key == 'w') {
      speedR.value = speed_val + 1
      ws.send("speed:0" + speedR.value);
      console.log(speedR.value);
    } else if (event.key == 's') {
      speedR.value = speed_val - 1
      ws.send("speed:0" + speedR.value);
    } else if (event.key == 'a') {
      steeringR.value = steering_val - 1
      ws.send("steering:0" + steeringR.value);
    } else if (event.key == 'ArrowUp') {
      cameraR.value += 1;
      ws.send("camera:0" + cameraR.value);
    } else if (event.key == 'ArrowDown') {
      cameraR.value += 1;
      ws.send("camera:0" + cameraR.value);
    } else if (event.key == 'd') {
      steeringR.value = steering_val + 1
      ws.send("steering:0" + steeringR.value);
    } else if (event.code == 'Space') {
      steeringR.value = 0
      ws.send("steering:0" + 0);
      stopSteering.style.opacity = "0.7"
    } else if (event.key == 'Enter') {
      stopEverything()
      stopAll.style.opacity = "0.7"
    } else if (event.key == '0') {
      cameraR.value = 0;
      ws.send("camera:0" + 0);
      resetCamera.style.opacity = "0.7"
    }
    outSpeed.innerText = speedR.value
    outSteering.innerText = steeringR.value
    outCamera.innerText = cameraR.value
  }, false);
  
  document.addEventListener("keyup", (event) => {
    if (event.code == 'Space') {
      stopSteering.style.opacity = "1"
    } else if (event.key === 'Enter') {
      stopAll.style.opacity = "1"
    } else if (event.key === '0') {
      resetCamera.style.opacity = "1"
    }
  })

  mSpeed.addEventListener("click", function () {
    speedRange.value -= 1;
    outSpeed.innerText = speedRange.value
    ws.send("speed:0" + speedR.value);
  }, false);

  pSpeed.addEventListener("click", function () {
    speedRange.value += 1;
    outSpeed.innerText = speedRange.value
    ws.send("speed:0" + speedR.value);
  }, false);


  mSteering.addEventListener("click", function () {
    steeringRange.value -= 1;
    outSteering.innerText = steeringRange.value
    ws.send("steering:0" + steeringR.value);
  }, false);

  pSteering.addEventListener("click", function () {
    steeringRange.value += 1;
    outSteering.innerText = steeringRange.value
    ws.send("steering:0" + steeringR.value);
  }, false);


  mCamera.addEventListener("click", function () {
    cameraRange.value -= 1;
    outCamera.innerText = cameraRange.value
    ws.send("camera:0" + cameraR.value);
  }, false);

  pCamera.addEventListener("click", function () {
    cameraRange.value += 1;
    outCamera.innerText = cameraRange.value
    ws.send("camera:0" + cameraR.value);
  }, false);

});

function prompt_alerts(description) {
  alert(description);

}
////////////////////////server websockets /////////////////////
ws.addEventListener("message", ({ data }) => {
  console.log("received-client: ", data);
})
ws.addEventListener("close", () => {
  srOFF();
})


///////////////////////////////GAMEPAD COMMANDS/////////////////////////////////
var gamePad;
var start
window.addEventListener("gamepadconnected", function (e) {
  gpON()
  console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
    e.gamepad.index, e.gamepad.id,
    e.gamepad.buttons.length, e.gamepad.axes.length);
  gameLoop();
});
window.addEventListener("gamepaddisconnected", e => {
  gpOFF()
  console.log("Gamepad disconnected from index %d: %s",
    e.gamepad.index, e.gamepad.id);
  window.cancelRequestAnimationFrame(start)

});
var valSpeed;
var valCamera = 0;
var valCameraUp = 0;
var pressedDown = false;
var pressedUp = false;
var valCameraDown = 0;
// var interval
function gameLoop() {

  var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
  if (!gamepads) {
    return;
  }

  gamePad = gamepads[0];
  if (gamePad.buttons[0].value == 1) {
    cameraR.value = 0;
    valCamera = 0;
    outCamera.innerText = 0;
  }

  valSpeedBack = Math.round(gamePad.buttons[6].value * -8);
  valSpeedBack = valSpeedBack < -5 ? -5 : valSpeedBack;
  valSpeedFront = Math.round(gamePad.buttons[7].value * 8);
  valSpeedFront = valSpeedFront > 5 ? 5 : valSpeedFront;
  valSpeed = valSpeedBack + valSpeedFront;
  if (speedR.value != valSpeed) {
    speedR.value = valSpeed;
    ws.send("speed:0" + speedR.value);
    outSpeed.innerText = speedR.value
  }
  var valSterring = Math.round(gamePad.axes[0] * 5);
  if (steeringR.value != valSterring) {
    steeringR.value = valSterring;
    ws.send("steering:0" + steeringR.value);
    outSteering.innerText = steeringR.value
  }
  if (gamePad.buttons[12].pressed) {
    if (pressedUp != true) {
      valCamera += 1;
    }
    pressedUp = true;
  } else { pressedUp = false; }

  if (gamePad.buttons[13].pressed) {
    if (pressedDown != true) {
      valCamera -= 1;
    }
    pressedDown = true;
  } else { pressedDown = false; }

  valCamera = valCamera > 5 ? 5 : valCamera;
  valCamera = valCamera < 0 ? 0 : valCamera;
  if (cameraR.value != valCamera) {
    cameraR.value = valCamera;
    ws.send("camera:0" + cameraR.value);
    outCamera.innerText = cameraR.value;
  }
  /* changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
   changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
   changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA*/
  start = window.requestAnimationFrame(gameLoop);

}
function handleOrientation(event) {
  var absolute = event.absolute;
  var alpha    = event.alpha;
  var beta     = event.beta;
  var gamma    = event.gamma;
  for(var prop in event){
    console.log(prop);
  }
 
  // Do stuff with the new orientation data
}
var s = document.getElementById("spped");
window.addEventListener("deviceorientation", function(e){
  s.innerHTML = "working";
  
});


