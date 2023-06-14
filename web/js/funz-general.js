function on(element){
    for (let i = 0; i < element.length; i++) {
        element[i].classList.add('on');
        element[i].classList.remove('off');
    }
}

function off(element){
    for (let i = 0; i < element.length; i++) {
        element[i].classList.add('off');
        element[i].classList.remove('on');
    }
}

var toggleButton = document.getElementsByClassName('toggle-joystick');
function openJoy(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleButton[i].classList.remove("bg-secondary");
        toggleButton[i].classList.add("bg-primary");
    }
}

function closeJoy(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleButton[i].classList.add("bg-secondary");
        toggleButton[i].classList.remove("bg-primary");  
    }
}

var toggleMicrophone = document.getElementsByClassName('toggle-microphone');
function openMic(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleMicrophone[i].classList.remove("bg-secondary");
        toggleMicrophone[i].classList.add("bg-primary");
    }
}

function openRec(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleMicrophone[i].classList.remove("bg-primary");
        toggleMicrophone[i].classList.add("bg-danger");
    }
}
function closeRec(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleMicrophone[i].classList.add("bg-primary");
        toggleMicrophone[i].classList.remove("bg-danger");
    }
}
function closeMic(){
    for (var i = 0; i < toggleButton.length; i++) {
        toggleMicrophone[i].classList.add("bg-secondary");
        toggleMicrophone[i].classList.remove("bg-primary");
    }
}

function remove_d_none(element){
    element.classList.remove("d-none");
}

function add_d_none(element){
    element.classList.add("d-none");
}