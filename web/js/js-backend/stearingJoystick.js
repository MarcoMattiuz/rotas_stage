var stearing_prec="";
var stearing_val="";

function setStearing(x, y){
    var accel=y;
    var steer=x;

    // console.log('Accel:', accel);
    // console.log('Steer:', steer);

    stearing_val = JSON.stringify({
        "accel": accel,
        "steer": -steer,
    });

    if (stearing_val === stearing_prec) {

    } else {
        stearing_prec = stearing_val;
        
        sendMessage(stearing_val);
    }
}