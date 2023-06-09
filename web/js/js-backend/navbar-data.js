var badgepad = document.getElementById('badge-pad');
var badgeserver = document.getElementById('badge-server');
var badgebatt = document.getElementById('badge-batt');

function checkNavServer(){
    if(connect)
    {
        //server
        badgeserver.classList.remove("bg-danger");
        badgeserver.classList.add("bg-success");
    }
    else
    {
        badgeserver.classList.remove("bg-success");
        badgeserver.classList.add("bg-danger");
    }
}

function checkNavPad(){
    if(controllerConnect)
    {
        //controller
        badgepad.classList.remove("bg-danger");
        badgepad.classList.add("bg-success");
    }
    else
    {
        badgepad.classList.remove("bg-success");
        badgepad.classList.add("bg-danger");
    }
}

function checkNavBatt(batteryLevel){
    if(batteryLevel==-1){
        badgebatt.className="";
        badgebatt.classList.add("badge");
        badgebatt.classList.add("bg-secondary");
        badgebatt.innerHTML='BATT';
    }else{
        badgebatt.innerHTML=batteryLevel+'%';
        if(batteryLevel>=0 && batteryLevel<=5){
            badgebatt.classList.remove("bg-secondary");
            badgebatt.classList.add("bg-danger");

        }else if(batteryLevel>5 && batteryLevel<=10){
            badgebatt.classList.remove("bg-secondary");
            badgebatt.classList.add("bg-warning");

        }else if(batteryLevel>10 && batteryLevel<=100){
            badgebatt.classList.remove("bg-secondary");
            badgebatt.classList.add("bg-success");
        }
    }
}

