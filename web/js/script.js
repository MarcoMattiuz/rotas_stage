var a = document.getElementById("a");
var b = document.getElementById("b");
var x = document.getElementById("x");
var y = document.getElementById("y");

var tr = document.getElementById("tr");
var tl = document.getElementById("tl");
var pr = document.getElementById("pr");
var pl = document.getElementById("pl");

var container = document.querySelector('.container');
var leftSquare = document.getElementById("L");
var rightSquare = document.getElementById("R");

var numA = 0;
var numB = 0;
var numX = 0;
var numY = 0;
var numR = 0;
var numL = 0;

var leftSquareX = 0;
var leftSquareY = 0;
var rightSquareX = 0;
var rightSquareY = 0;

update();

function update() {
    var gamepads = navigator.getGamepads();

    for (var i = 0; i < gamepads.length; i++) {
        var gamepad = gamepads[i];

        if (gamepad && gamepad.id === "Xbox 360 Controller (XInput STANDARD GAMEPAD)") {
            var buttons = gamepad.buttons;
            var axes = gamepad.axes;

            if (buttons[0].pressed) {
                numA++;
            }
            if (buttons[1].pressed) {
                numB++;
            }
            if (buttons[2].pressed) {
                numX++;
            }
            if (buttons[3].pressed) {
                numY++;
            }

            if (buttons[5].pressed) {
                numR++;
            }
            if (buttons[4].pressed) {
                numL++;
            }

            if (buttons[7].pressed) {
                var val = buttons[7].value - 0.09
                //console.log(val);
                if (val < 0) val = 0; 
                var ris=(val*1023)/0.91;

                tr.innerHTML = "Trigger R: " + Math.floor(ris);
            } else {
                tr.innerHTML = "Trigger R: 0";
            }
            
            if (buttons[6].pressed) {
                var val = buttons[6].value - 0.09

                //console.log(val);
                if (val < 0) val = 0; 
                var ris=(val*1023)/0.91;

                tl.innerHTML = "Trigger L: " + Math.floor(ris);
            } else {
                tl.innerHTML = "Trigger L: 0";
            }

            a.innerHTML = "Pulsante A: " + numA;
            b.innerHTML = "Pulsante B: " + numB;
            x.innerHTML = "Pulsante X: " + numX;
            y.innerHTML = "Pulsante Y: " + numY;

            pr.innerHTML = "Pulsante R: " + numR;
            pl.innerHTML = "Pulsante L: " + numL;

            leftSquareX = axes[0] * 150; 
            leftSquareY = axes[1] * 150;
            leftSquare.style.transform = `translate(${leftSquareX}px, ${leftSquareY}px)`;

            rightSquareX = axes[2] * 150;
            rightSquareY = axes[3] * 150;
            rightSquare.style.transform = `translate(${rightSquareX}px, ${rightSquareY}px)`;
        }
    }

    requestAnimationFrame(update);
}