let LOutline = document.getElementById("LOutline");
let ROutline = document.getElementById("ROutline");

function pitagora(x, y) {
    return Math.sqrt(x*x+y*y);
}

function updateGamepadStatus() {
    let gamepads = navigator.getGamepads();
   
    for (var i = 0; i < gamepads.length; i++) {
        let gamepad = gamepads[i];

        if (gamepad&&connect) {
            let buttons = gamepad.buttons;
            let axes = gamepad.axes;
            let LeftStick= document.getElementById("LeftStick");//cx 101 full sinistra, 113 centrale val di default, 125 full destra e cy 148 full sopra, 160 default, 172 full sotto
            
            let Up= document.getElementById("DUp");
            let Down= document.getElementById("DDown");
            let Left= document.getElementById("DLeft");
            let Right= document.getElementById("DRight");

            let A= document.getElementById("BBottom");
            let B= document.getElementById("BRight");
            let X= document.getElementById("BLeft");
            let Y= document.getElementById("BTop");

            let LT= document.getElementById("L2");
            let RT= document.getElementById("R2");

            let LB= document.getElementById("L1");
            let RB= document.getElementById("R1");

            let LMeta= document.getElementById("LMeta");
            let RMeta= document.getElementById("RMeta");

            LeftStick.setAttribute("cx", 113 + (axes[0] * 12));
            LeftStick.setAttribute("cy", 160 + (axes[1] * 12));
            LeftStick.setAttribute("fill", "rgba(0,0,0,"+ Math.abs(pitagora(axes[0], axes[1]))+")");
            RightStick.setAttribute("cx", 278 + (axes[2] * 12));
            RightStick.setAttribute("cy", 238 + (axes[3] * 12));
            RightStick.setAttribute("fill", "rgba(0,0,0,"+ Math.abs(pitagora(axes[2], axes[3]))+")");

            Up.setAttribute("fill", val(buttons[12].pressed));
            Down.setAttribute("fill", val(buttons[13].pressed));
            Left.setAttribute("fill", val(buttons[14].pressed));
            Right.setAttribute("fill", val(buttons[15].pressed));

            A.setAttribute("fill", val(buttons[0].pressed));
            B.setAttribute("fill", val(buttons[1].pressed));
            X.setAttribute("fill", val(buttons[2].pressed));
            Y.setAttribute("fill", val(buttons[3].pressed));

            LT.setAttribute("fill", "rgba(0,0,0,"+buttons[6].value+")");
            RT.setAttribute("fill", "rgba(0,0,0,"+buttons[7].value+")");

            LB.setAttribute("fill", val(buttons[4].pressed));
            RB.setAttribute("fill", val(buttons[5].pressed));
            
            LMeta.setAttribute("fill", val(buttons[8].pressed));
            RMeta.setAttribute("fill", val(buttons[9].pressed));
         
        }    
    }
    requestAnimationFrame(updateGamepadStatus); 
}

function val(pressed){
    if(pressed){
        return "rgba(0,0,0,1)";
    }
    else{
        return "rgba(0,0,0,0)";
    }
}



async function lgbt(){
    let letters = "0123456789ABCDEF";
    let color = "#";

    for(var i=0; i<6; i++)
    {
        color += letters[Math.floor(Math.random()*16)];
    }

    LOutline.setAttribute("stroke", color);
    ROutline.setAttribute("stroke", color);

}

async function resetColor(){
    LOutline.setAttribute("stroke", "hsl(210,50%,85%)");
    ROutline.setAttribute("stroke", "hsl(210,50%,85%)");
}





