var progressBar = document.getElementById("progress");
var cent = document.getElementById("cent");

function updateBattery(batteryLevel) {
    progressBar.style.width = batteryLevel + "%";
    cent.innerHTML="<span>"+parseInt(batteryLevel) + "%<span>";
}

function reset_battery(){
    progressBar.style.width = 0 + "%";
    cent.innerHTML='<span id="batt" class="error-message"> Nessuna batteria</span>';           
}