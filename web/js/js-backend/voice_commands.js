var toggleMicrophone = document.getElementsByClassName('toggle-microphone');

var rec=false;
var text;
var sound;

var json_command={};

for (let i = 0; i < toggleMicrophone.length; i++) {
  toggleMicrophone[i].addEventListener('click', function() {
    if(connect&&!controllerConnect){
      if(!rec){
        openRec();
        rec=true;

        voice_commands();
        recognition.start();
        
      }else{
        closeRec();
        json_command={};
        rec=false;

        //console.log("chiuso");
        recognition.stop();
      }  
    }
  });
}


function voice_commands(){
    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        //console.log("rec");
        recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'it-IT';

        recognition.onresult = function(event) {
            text = event.results[0][0].transcript;
            text = text.toLowerCase();
            console.log(text);
            
            if (text.includes("fermo")||text.includes("stop")) {
                //changeAudioSource("stop");
                //playAudio();
                json_command={
                    "left":0,
                    "right":0,
                    "sound":"stop"
                }
                rec=false;

                sendMessage(JSON.stringify(json_command));
            }
            else
            {
              json_command=command(text);
              sendMessage(JSON.stringify(json_command));
            }
            console.log(JSON.stringify(json_command));
        };

        recognition.onend = function() {
          closeRec();
          json_command={};
          rec=false;

          //console.log("chiuso");
          recognition.stop();
        };
        
    } else {
        console.error('Il tuo browser non supporta l\'API di riconoscimento vocale.');
    }   
}


