/*IMG*/
var camElement = document.getElementById("cam");
var loading_cam = document.getElementById("loading_cam");
var detect = document.getElementById("detect");

function openCam(){
    
    camElement.innerHTML='<img id="video-embed" style="max-height:100%; max-width:100%; min-height:100%; min-width:100%;" />';
    
    add_d_none(loading_cam);
    remove_d_none(camElement);

    document.getElementById("video-embed").classList.add('rounded-2');
    camconnect=true;
}

function updateCam(src) {
    console.log("frame");
    document.getElementById("video-embed").src = src;
}

function reset_cam(){
    //remove_d_none(loading_cam);
    //add_d_none(camElement);

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
