var camElement = document.getElementById("cam");
var loading_cam = document.getElementById("loading_cam");
var detect = document.getElementById("detect");
var canvas;

var restart = document.getElementsByClassName("restart-cam");

restart[0].addEventListener('click', function() {
    if(connect){
        sendMessage(JSON.stringify({"oak":true}));
    }
});

function openCam(){
    camElement.innerHTML='<canvas id="video" style="max-height:100%; max-width:100%; min-height:100%; min-width:100%;"></canvas>';
    
    add_d_none(loading_cam);
    remove_d_none(camElement);

    document.getElementById("video").classList.add('rounded-2');
    camconnect=true;
    canvas = document.getElementById("video");
}

function updateCam(src) {
    var ctx = canvas.getContext("2d");

    var img = new Image();
    img.onload = function () {
        canvas.width = img.width;
        canvas.height = img.height;

        ctx.drawImage(img, 0, 0);
    };
    img.src = src;
}

function drawRectangle(x1, y1, x2, y2) {
    var ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.lineWidth = "2";
    ctx.strokeStyle = "red";
    ctx.rect(x1, y1, x2 - x1, y2 - y1);
    ctx.stroke();
}

function reset_cam(){
    camElement.innerHTML='';
    camconnect=false; 

    detect.classList.add('error-message');
    detect.innerHTML = 'Impossibile recuperare la videocamera';
}

function read_dets(data){
    if(data){

        var str="";
        var isLast = false;

        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                if (isLast) {
                str += ", ";
                }
                str += key + ": " + data[key];
                isLast = true;
            }
        }

        detect.classList.remove('error-message');
        detect.innerHTML = str;
    }else{
        if(camconnect){
            detect.classList.add('error-message');
            detect.innerHTML = "Nessuna rilevazione";
        }
    }
}
