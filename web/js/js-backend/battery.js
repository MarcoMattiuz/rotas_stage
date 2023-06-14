var progressBar = document.getElementsByClassName("progress");
var cent = document.getElementsByClassName("cent");

function updateBattery(batteryLevel) {
    for (let i = 0; i < progressBar.length && i < cent.length; i++) {
        progressBar[i].style.width = batteryLevel + "%";
        cent[i].innerHTML='<span class="batt">'+parseInt(batteryLevel) + '%<span>';

        if(batteryLevel>=0 && batteryLevel<=5){
            progressBar[i].style.backgroundColor="#d33333";

        }else if(batteryLevel>5 && batteryLevel<=10){
            progressBar[i].style.backgroundColor="#e2f026";

        }else if(batteryLevel>10 && batteryLevel<=100){
            progressBar[i].style.backgroundColor="#4CAF50";
        }
    }
    checkNavBatt(batteryLevel);
}

function reset_battery(){
    for (let i = 0; i < progressBar.length && i < cent.length; i++) {
        progressBar[i].style.width = 0 + "%";
        cent[i].innerHTML='<span class="batt error-message"> Nessuna batteria</span>';    
    } 
    checkNavBatt(-1);
}
