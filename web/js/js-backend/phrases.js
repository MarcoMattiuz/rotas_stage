const comandi= {};


comandi["destra avanti veloce"] = {
    "left": 0,
    "right": 1023,
    "sound": "a_dx_v"
}; // Ok vado avanti a destra veloce!

comandi["destra avanti lento"] = {
    "left": 0,
    "right": 500,
    "sound": "a_dx_l"
}; // Ok vado avanti a destra lento!

comandi["destra indietro veloce"] = {
    "left": 0,
    "right": -1023,
    "sound": "i_dx_v"
}; // Ok vado indietro a destra veloce!

comandi["destra indietro lento"] = {
    "left": 0,
    "right": -500,
    "sound": "i_dx_l"
}; // Ok vado indietro a destra lento!

comandi["sinistra avanti veloce"] = {
    "left": 1023,
    "right": 0,
    "sound": "a_sx_v"
}; // Ok vado avanti a sinistra veloce!

comandi["sinistra avanti lento"] = {
    "left": 500,
    "right": 0,
    "sound": "a_sx_l"
}; // Ok vado avanti a sinistra lento!

comandi["sinistra indietro veloce"] = {
    "left": -1023,
    "right": 0,
    "sound": "i_sx_v"
}; // Ok vado indietro a sinistra veloce!

comandi["sinistra indietro lento"] = {
    "left": -500,
    "right": 0,
    "sound": "i_sx_l"
}; // Ok vado indietro a sinistra lento!

comandi["entrambi avanti veloce"] = {
    "left": 1023,
    "right": 1023,
    "sound": "a_e_v"
}; // Ok vado avanti in modalità cingolato veloce!

comandi["entrambi avanti lento"] = {
    "left": 500,
    "right": 500,
    "sound": "a_e_l"
}; // Ok vado avanti in modalità cingolato lento!

comandi["entrambi indietro veloce"] = {
    "left": -1023,
    "right": -1023,
    "sound": "i_e_v"
}; // Ok vado indietro in modalità cingolato veloce!

comandi["entrambi indietro lento"] = {
    "left": -500,
    "right": -500,
    "sound": "i_e_l"
}; // Ok vado indietro in modalità cingolato lento!

/*
var audio = document.getElementById("myAudio");
var source = document.getElementById("audioSource");

function changeAudioSource(src) {
    source.src = "audio/"+src+".mp3";
    audio.load();
}

function playAudio(){
    audio.play();
}*/

function command(testo) {
    for (var key in comandi) {
        if (testo === key) {
            //console.log("Comando:", key);
            //console.log("Valore:", comandi[key]);
            return comandi[key];
        }
    }
}