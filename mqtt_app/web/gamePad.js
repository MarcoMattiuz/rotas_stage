// import { changeValue_Text, speedR } from "./main";


// var gamePad;
// var start;
// console.log("ciao")
// window.addEventListener("gamepadconnected", e => {

//     console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
//         e.gamepad.index, e.gamepad.id,
//         e.gamepad.buttons.length, e.gamepad.axes.length);
//     gamePad = navigator.getGamepads()[e.gamepad.index]
// });
// window.addEventListener("gamepaddisconnected", e => {
//     console.log("Gamepad disconnected from index %d: %s",
//         e.gamepad.index, e.gamepad.id);
//     cancelRequestAnimationFrame(start);
//     gamePad = null;
// });

// function gameLoop() {

//     if (!gamepad) {
//         return;
//     }
//     if (gamePad.buttons[0] == 1) {
//         changeValue_Text(2, 0) //--> STEERING
//         changeValue_Text(1, 0) //--> SPEED
//     }

//     console.log(gamePad.buttons.axes[2] * 5)

//     changeValue_Text(2, gamePad.buttons.axes[2] * 5) //--> STEERING
//     changeValue_Text(1, gamePad.buttons.axes[3] * 5) //--> SPEED
//     changeValue_Text(3, gamePad.buttons.axes[0] * 5) //--> CAMERA
//     start = requestAnimationFrame(gameLoop);
// }
