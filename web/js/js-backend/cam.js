var cam = document.getElementById("cam");

function openCam(){
    cam.innerHTML='<img id="video-embed" style="max-height:100%; max-width:100%; min-height:100%; min-width:100%;" />';
    document.getElementById("video-embed").classList.add('rounded-2');
    camconnect=true;
}

function updateCam(src) {
    console.log("update");
    document.getElementById("video-embed").src = src;
}

function reset_cam(){
    console.log("reset");
    cam.innerHTML='<span class="error-message">Impossibile recuperare la videocamera</span>';      
}