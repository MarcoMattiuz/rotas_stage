const speedR = document.getElementById("speedRange"); //
const steeringR = document.getElementById("steeringRange"); //
const stopAll = document.getElementById("stopAll");
const stopSteering = document.getElementById("stopSteering");
const speechToggle = document.getElementById("speech-toggle");
speechToggle.checked = true; //è al contrario ;)
let outSpeed = document.getElementById("outSpeed");
let outSteering = document.getElementById("outSteering");
let on_sr = document.getElementById("on_sr");
let off_sr = document.getElementById("off_sr");
let on_gp = document.getElementById("on_gp");
let off_gp = document.getElementById("off_gp");
var mSpeed = document.getElementById("mSpeed");
var pSpeed = document.getElementById("pSpeed");
var mSteering = document.getElementById("mSteering");
var pSteering = document.getElementById("pSteering");
var msg = document.getElementById("video-embed");
var videoDisp = document.getElementById("video-display")
var w = window.innerWidth;
var h = window.innerHeight;
window.addEventListener("resize", () => {
  var w = window.innerWidth;
  var h = window.innerHeight;
  if (w <= 750) {
    videoDisp.style.display = 'none'
  } else {
    videoDisp.style.display = 'block'
  }
})
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
  ws.send(JSON.stringify({ "speed": 0 }));
  ws.send(JSON.stringify({ "steering": 0 }));
  outSpeed.innerText = speedR.value
  outSteering.innerText = steeringR.value;
}


/* *************** */
gpOFF()
srOFF()
var ws = new WebSocket("wss://rover.rotas.eu/api/websocket");

ws.addEventListener("open", () => {
  console.log("we are connected");
  ws.send(JSON.stringify({ "photo": 1 }))
  srON()
  ws.onerror = function (e) {
    Console.log('WebSocket error: ' + e.code)
    console.log(e)
  }
  ws.addEventListener("close", () => {
    console.log("server is down");

    srOFF();
  });
  speedR.addEventListener("change", () => {
    ws.send(JSON.stringify({ "speed": speedR.value }));
    outSpeed.innerText = speedR.value;
  });
  steeringR.addEventListener("change", () => {
    ws.send(JSON.stringify({ "steering": steeringR.value }));
    outSteering.innerText = steeringR.value;
  });

  stopAll.addEventListener("click", () => {
    stopEverything()
  })
  stopSteering.addEventListener("click", () => {
    steeringR.value = 0
    outSteering.innerText = steeringR.values
    ws.send(JSON.stringify({ "steering": steeringR.value }));
  })


  document.addEventListener('keydown', (event) => {
    let speed_val = parseInt(speedR.value)
    let steering_val = parseInt(steeringR.value)

    if (event.key == 'w') {
      speedR.value = speed_val + 1

      ws.send(JSON.stringify({ "speed": speedR.value }));
      console.log(speedR.value);
    } else if (event.key == 's') {
      speedR.value = speed_val - 1
      ws.send(JSON.stringify({ "speed": speedR.value }));
    } else if (event.key == 'a') {
      steeringR.value = steering_val - 1
      ws.send(JSON.stringify({ "steering": steeringR.value }));
    } else if (event.key == 'd') {
      steeringR.value = steering_val + 1
      ws.send(JSON.stringify({ "steering": steeringR.value }));
    } else if (event.code == 'Space') {
      steeringR.value = 0
      ws.send(JSON.stringify({ "steering": 0 }));
      stopSteering.style.opacity = "0.7"
    } else if (event.key == 'Enter') {
      stopEverything()
      stopAll.style.opacity = "0.7"
    } else if (event.key == 'o') {
      ws.send(JSON.stringify({ "photo": 1 }));
    }
    outSpeed.innerText = speedR.value
    outSteering.innerText = steeringR.value
  }, false);

  document.addEventListener("keyup", (event) => {
    if (event.code == 'Space') {
      stopSteering.style.opacity = "1"
    } else if (event.key === 'Enter') {
      stopAll.style.opacity = "1"
    }
  })

  mSpeed.addEventListener("click", function () {
    speedRange.stepDown();
    outSpeed.innerText = speedRange.value
    ws.send(JSON.stringify({ "speed": speedR.value }));
  }, false);

  pSpeed.addEventListener("click", function () {
    speedRange.stepUp();
    outSpeed.innerText = speedRange.value
    ws.send(JSON.stringify({ "speed": speedR.value }));
  }, false);


  mSteering.addEventListener("click", function () {
    steeringRange.value -= 1;
    outSteering.innerText = steeringRange.value
    ws.send(JSON.stringify({ "steering": steeringR.value }));
  }, false);

  pSteering.addEventListener("click", function () {
    steeringRange.value += 1;
    outSteering.innerText = steeringRange.value
    ws.send(JSON.stringify({ "steering": steeringR.value }));
  }, false);


  /////////////////////////////////////// VOICE COMMANDS ///////////////////////////////////////

  function sleep(milliseconds) {
    var start = new Date().getTime();
    for (var i = 0; ; i++) {
      if ((new Date().getTime() - start) > milliseconds) {
        break;
      }
    }
  }

  var max_speed = 3;
  var direzione = "";
  var direzione_old = "";

  recognition = new webkitSpeechRecognition();
  recognition.lang = "it";
  recognition.continuous = true;
  recognition.interimResults = true;

  recognition.onresult = function (event) {
    text = "";
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (!event.results[i].isFinal) {
        text = event.results[i][0].transcript;
      }
    }
    text = text.toLowerCase();
    // console.log(text);
    message = text.split(" ");

    for (let i = 0; i < message.length; i++) {
      text = message[i];
      if (text.includes("avanti") || text.includes("attacca")) {
        direzione = "avanti";
      } else if (text.includes("dietro")) {
        direzione = "indietro";
      } else if (text.includes("destra")) {
        direzione = "destra";
      } else if (text.includes("sinistr")) {
        direzione = "sinistra";
      } else if (text.includes("fermo") || text.includes("stop")) {
        direzione = "stop";
      }
      else if (text.includes("giro") || text.includes("tondo")) {
        direzione = "giro";
      } else if (text.includes("cod") || text.includes("ciao")) {
        direzione = "scodinzola";
      }
      else if (text.includes("veloce")) {
        direzione = "veloce";
      }
      else if (text.includes("lento")) {
        direzione = "lento";
      }
      
    }

    if (direzione != direzione_old) {
      direzione_old = direzione;
      if (direzione == "avanti") {    // AVANTI
        ws.send(JSON.stringify({ "speed": max_speed }));
        ws.send(JSON.stringify({ "steering": 0 }));
      } else if (direzione == "indietro") {    // INDIETRO
        ws.send(JSON.stringify({ "speed": -max_speed }));
        ws.send(JSON.stringify({ "steering": 0 }));
      } else if (direzione == "destra") {    // DESTRA
        ws.send(JSON.stringify({ "speed": max_speed }));
        ws.send(JSON.stringify({ "steering": 5 }));
        sleep(1300);
        ws.send(JSON.stringify({ "speed": 0 }));
        ws.send(JSON.stringify({ "steering": 0 }));
      } else if (direzione == "sinistra") {    // SINISTRA
        ws.send(JSON.stringify({ "speed": max_speed }));
        ws.send(JSON.stringify({ "steering": -5 }));
        sleep(1300);
        ws.send(JSON.stringify({ "speed": 0 }));
        ws.send(JSON.stringify({ "steering": 0 }));
      } else if (direzione == "stop") {    // STOP
        ws.send(JSON.stringify({ "speed": 0 }));
        ws.send(JSON.stringify({ "steering": 0 }));
      }
      else if (direzione == "giro") {    // GIRO
        ws.send(JSON.stringify({ "speed": max_speed }));
        ws.send(JSON.stringify({ "steering": 5 }));
        sleep(5000);
        ws.send(JSON.stringify({ "speed": 0 }));
        ws.send(JSON.stringify({ "steering": 0 }));

      } else if (direzione == "scodinzola") {    // SCODINZOLA
        for (let i = 0; i < 4; i++) {
          ws.send(JSON.stringify({ "speed": max_speed }));
          ws.send(JSON.stringify({ "steering": 5 }));
          sleep(200);
          ws.send(JSON.stringify({ "speed": max_speed }));
          ws.send(JSON.stringify({ "steering": -5 }));
          sleep(200);
        }
        ws.send(JSON.stringify({ "speed": 0 }));
        ws.send(JSON.stringify({ "steering": 0 }));
      }
      else if(direzione == "veloce"){
        max_speed = 5;
      }
      else if(direzione == "lento"){
        max_speed = 3;
      }
    }
    direzione = "-";

    // document.getElementById("textarea").value = direzione;
    console.log(direzione)
  };



  speechToggle.addEventListener("change", () => {
    if (!speechToggle.checked) {
      console.log("riconoscimento vocale ON")
      recognition.start();
    } else {
      console.log("riconoscimento vocale OFF")
      recognition.stop();
    }
  })


  /////////////////////////////////////// GAMEPAD COMMANDS ///////////////////////////////////////
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
  var pressedDown = false;
  var pressedUp = false;
  // var interval
  function gameLoop() {

    var gamepads = navigator.getGamepads ? navigator.getGamepads() : (navigator.webkitGetGamepads ? navigator.webkitGetGamepads() : []);
    if (!gamepads) {
      return;
    }

    gamePad = gamepads[0];
    if (gamePad.buttons[0].value == 1) {
      cameraR.value = 0;
      outCamera.innerText = 0;
    }

    valSpeedBack = Math.round(gamePad.buttons[6].value * -8);
    valSpeedBack = valSpeedBack < -5 ? -5 : valSpeedBack;
    valSpeedFront = Math.round(gamePad.buttons[7].value * 8);
    valSpeedFront = valSpeedFront > 5 ? 5 : valSpeedFront;
    valSpeed = valSpeedBack + valSpeedFront;
    if (speedR.value != valSpeed) {
      speedR.value = valSpeed;
      ws.send(JSON.stringify({ "speed": speedR.value }));
      outSpeed.innerText = speedR.value
    }
    var valSterring = Math.round(gamePad.axes[0] * 5);
    if (steeringR.value != valSterring) {
      steeringR.value = valSterring;
      ws.send(JSON.stringify({ "steering": steeringR.value }));
      outSteering.innerText = steeringR.value
    }
    if (gamePad.buttons[12].pressed) {
      if (pressedUp != true) {
        valCamera += 1;
      }
      pressedUp = true;
    } else pressedUp = false;

    if (gamePad.buttons[13].pressed) {
      if (pressedDown != true) {
        valCamera -= 1;
      }
      pressedDown = true;
    } else pressedDown = false;

    valCamera = valCamera > 5 ? 5 : valCamera;
    valCamera = valCamera < 0 ? 0 : valCamera;
    if (cameraR.value != valCamera) {
      cameraR.value = valCamera;
      ws.send(JSON.stringify({ "camera": cameraR.value }));
      outCamera.innerText = cameraR.value;
    }
    /* changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
     changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
     changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA*/
    start = window.requestAnimationFrame(gameLoop);
  }
});

function prompt_alerts(description) {
  alert(description);

}
/////////////////////////////////////// server websockets ///////////////////////////////////////
ws.addEventListener("message", ({ data }) => {
  photo = JSON.parse(data);
  if (photo.hasOwnProperty("photo")) {
    console.log(photo['photo']);
    msg.src = 'data:image/jpg;base64,' + photo['photo'];
  }
});



