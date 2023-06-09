var camElement = document.getElementById("cam");
var loading_cam = document.getElementById("loading_cam");
var detect = document.getElementById("detect");

/*function cam(img){
    if (img === null) {        
        //detect.classList.add('error-message');
        //detect.innerHTML = 'Impossibile recuperare la videocamera';
        console.log(null);
        return;
    }else{
        if(!camconnect){
            openCam();
        }
        //var src = 'data:image/jpg;base64,' + json.img;
        updateCam(img);
    }
}

function openCam(){
    loading_cam.classList.add("d-none");
    camElement.classList.remove("d-none");

    camElement.innerHTML='<video id="player"></video>';
    camconnect=true;

    detect.classList.remove('error-message');
    detect.innerHTML = 'People: ....';
}

function updateCam(src) {
    
    detect.classList.remove('error-message');
    detect.innerHTML = 'People: ....';
}

function reset_cam(){
    loading_cam.classList.remove("d-none");
    camElement.classList.add("d-none");

    camElement.innerHTML='';
    camconnect=false; 

    detect.classList.add('error-message');
    detect.innerHTML = 'Impossibile recuperare la videocamera';
}*/

/*
JMUXER
function cam(img){
    if (img === null) {        
        //detect.classList.add('error-message');
        //detect.innerHTML = 'Impossibile recuperare la videocamera';
        console.log(null);
        return;
    }else{
        if(!camconnect){
            openCam();
        }
        //var src = 'data:image/jpg;base64,' + json.img;
        updateCam(img);
    }
}

function openCam(){
    loading_cam.classList.add("d-none");
    camElement.classList.remove("d-none");

    camElement.innerHTML='<video id="player"></video>';
    jmuxer = new JMuxer({
        node: 'player',
        mode: 'video',
        flushingTime: 1000,
        fps: 30,
        debug: true
    });
    
    camconnect=true;

    detect.classList.remove('error-message');
    detect.innerHTML = 'People: ....';
}

function updateCam(src) {
    jmuxer.feed({
        video: new Uint8Array(src)
    });

    detect.classList.remove('error-message');
    detect.innerHTML = 'People: ....';
}

function reset_cam(){
    loading_cam.classList.remove("d-none");
    camElement.classList.add("d-none");

    camElement.innerHTML='';
    camconnect=false; 

    detect.classList.add('error-message');
    detect.innerHTML = 'Impossibile recuperare la videocamera';
}*/

/*
IMG*/

function openCam(){
    loading_cam.classList.add("d-none");
    camElement.classList.remove("d-none");

    camElement.innerHTML='<img id="video-embed" style="max-height:100%; max-width:100%; min-height:100%; min-width:100%;" />';
    document.getElementById("video-embed").classList.add('rounded-2');
    camconnect=true;
}

function updateCam(src) {
    console.log("frame");
    document.getElementById("video-embed").src = src;
}

function reset_cam(){
    loading_cam.classList.remove("d-none");
    camElement.classList.add("d-none");

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
