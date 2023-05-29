function updateBattery(batteryLevel) {
    var progressBar = document.getElementById("progress");
    var cent = document.getElementById("cent");

    progressBar.style.width = batteryLevel + "%";
    cent.innerHTML= parseInt(batteryLevel) + "%";
  }
  