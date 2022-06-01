const speedR = document.getElementById("speedRange"); //
const cameraR = document.getElementById("cameraRange"); //
const steeringR = document.getElementById("steeringRange"); //
const stopAll = document.getElementById("stopAll");
const stopSteering = document.getElementById("stopSteering");
const resetCamera = document.getElementById("resetCamera")
let outSpeed = document.getElementById("outSpeed");
let outCamera = document.getElementById("outCamera");
let outSteering = document.getElementById("outSteering");
console.log("CIAO")
console.log(speedR)



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
const ws = new WebSocket("ws://pi.local:8000");
// ws.addEventListener("open", () => {
console.log("we are connected");

speedR.addEventListener("change", () => {
  console.log(speedR.value);
  ws.send("speed:0" + speedR.value);
  outSpeed.innerText = speedR.value
});
cameraR.addEventListener("change", () => {
  ws.send("camera:0" + cameraR.value);
  outCamera.innerText = cameraR.value
});
steeringR.addEventListener("change", () => {
  ws.send("steering:0" + steeringR.value);
  outSteering.innerText = steeringR.value
});

stopAll.addEventListener("click", () => {
  stopEverything()
})
stopSteering.addEventListener("click", () => {
  steeringR.value = 0

  outSteering.innerText = steeringR.value
})
resetCamera.addEventListener("click", () => {
  cameraR.value = 0;

  outCamera.innerText = cameraR.value
})
document.addEventListener('keydown', (event) => {
  let speed_val = parseInt(speedR.value)
  let steering_val = parseInt(steeringR.value)

  if (event.key === 'ArrowUp' || event.key == 'w') {
    speedR.value = speed_val + 1
    ws.send("speed:0" + speedR.value);
    console.log(speedR.value);

  }
  else if (event.key == 'ArrowDown' || event.key == 's') {
    speedR.value = speed_val - 1
    ws.send("speed:0" + speedR.value);

  }
  else if (event.key == 'ArrowLeft' || event.key == 'a') {
    steeringR.value = steering_val - 1
    ws.send("steering:0" + steeringR.value);

  }
  else if (event.key == 'ArrowRight' || event.key == 'd') {
    steeringR.value = steering_val + 1
    ws.send("steering:0" + steeringR.value);
  }
  else if (event.code == 'Space') {
    steeringR.value = 0
    ws.send("steering:0" + 0);
    stopSteering.style.background = "red"
  } else if (event.key === 'Enter') {
    stopEverything()
    stopAll.style.background = "red"
  } else if (event.key === '0') {
    cameraR.value = 0;
    ws.send("steering:0" + 0);
    resetCamera.style.background = "red"
  }
  outSpeed.innerText = speedR.value
  outSteering.innerText = steeringR.value
  outCamera.innerText = cameraR.value
}, false);

document.addEventListener("keyup", (event) => {
  if (event.code == 'Space') {
    stopSteering.style.background = "#cf0303"
  } else if (event.key === 'Enter') {
    stopAll.style.background = "#cf0303"
  } else if (event.key === '0') {
    resetCamera.style.background = "#cf0303"
  }
})

// });
// ws.addEventListener("message", ({ data }) => {
//   console.log("received-client: ", data);
// })



function prompt_alerts(description) {
  alert(description);
}

// comandi da tastiera


// // COMANDI DA GAMEPAD
// var gamePad;
// var start;

// window.addEventListener("gamepadconnected", function (e) {
//   console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
//     e.gamepad.index, e.gamepad.id,
//     e.gamepad.buttons.length, e.gamepad.axes.length);
//   gameLoop();
// });
// window.addEventListener("gamepaddisconnected", e => {
//   console.log("Gamepad disconnected from index %d: %s",
//     e.gamepad.index, e.gamepad.id);
//   window.cancelRequestAnimationFrame(start);

//   // window.addEventListener("gamepadconnected", function (e) {
//   //   console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
//   //     e.gamepad.index, e.gamepad.id,
//   //     e.gamepad.buttons.length, e.gamepad.axes.length);
//   //   gameLoop();
//   // });
//   // window.addEventListener("gamepaddisconnected", e => {
//   //   console.log("Gamepad disconnected from index %d: %s",
//   //     e.gamepad.index, e.gamepad.id);
//   //   window.cancelRequestAnimationFrame(start);

//   // });
//   // var interval;

//   function gameLoop() {
//     // console.log(gamePad);
//     // console.log("asdasdasdasdasd");

//     // function gameLoop() {
//     //   // console.log(gamePad);
//     //   // console.log("asdasdasdasdasd");

//     if (gamePad.buttons[0].value == 1) {
//       console.log(gamePad.buttons[0])
//     }
//     var valSpeed = Math.round(gamePad.axes[1] * -5);
//     if (speedR.value != valSpeed) {
//       speedR.value = valSpeed;
//       console.log(valSpeed);
//       eel.changeSpeed(speed = speedR.value);

//     }
//     var valSterring = Math.round(gamePad.axes[2] * 5);
//     if (steeringR.value != valSterring) {
//       steeringR.value = valSterring;
//       eel.changeSteering(steering = steeringR.value);
//     }




//     /* changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
//      changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
//      changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA*/
//     start = window.requestAnimationFrame(gameLoop);
//   }
// })
