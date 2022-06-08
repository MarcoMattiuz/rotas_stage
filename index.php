<?php
session_start();

if(isset($_SESSION["login"])==null){
  header("location: login.php");
}

?>
<!DOCTYPE html>
<html lang="it">

<head>
  <meta charset="UTF-8" />
  <meta http-equiv="X-UA-Compatible" content="IE=edge" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="./web/assets/roundSlider-1.6.1/src/roundslider.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.css" />
  <link rel="stylesheet" href="web/src_CSS/main.css" />
</head>

<body>
  <main>
    <section>
      <div class="info">
        <img src="./web/assets/Logo_rotas.png" alt="logo rotas">
        <div class="gamepad-connection">
          <h2>Gamepad <br> connection </h2>
          <div class="connection_indicator on" id="on_gp"></div>
          <div class="connection_indicator off" id="off_gp"></div>
        </div>
        <div class="server-connection">
          <h2>Rover <br> connection</h2>
          <div class="connection_indicator on" id="on_sr"></div>
          <div class="connection_indicator off" id="off_sr"></div>
        </div>
      </div>
        <div class="video_container">
          <!-- <embed src="http://192.168.8.40:8080" class="videofeed" class="video" /> -->
          <video autoplay="true" id="videoElement"></video>
        </div>
        <!-- test CAMERA -->
        <script>
          let video = document.getElementById("videoElement")

          if(navigator.mediaDevices.getUserMedia){
            navigator.mediaDevices.getUserMedia({video : true})
              .then(function (stream){
                video.srcObject = stream;
              })
              .catch(function (error){
                console.log("error");
              })
          }else{
            console.log("Video not supported")
          }
        </script>

        <div class="controls"> 
          <div class="sliders_wrap box">
            <div class="title-slider out"> SPEED <div id="outSpeed">0</div> </div>
              <div class="range-box vertical">        
                <div title="Decrease" class="control-minus" id="mSpeed">-</div>    
                <input id="speedRange"  type="range" min="-5" max="5" value="0" autocomplete="off">    
                <span class="legend-min">-5</span>
                <span class="legend-max">5</span>
                <div title="increase" class="control-plus" id="pSpeed">+</div>
              </div>
            <div class="title-slider out"> STEERING <div id="outSteering">0</div> </div>
              <div class="range-box">        
                <div title="Decrease" class="control-minus" id="mSteering">-</div>    
                <input id="steeringRange"  type="range" min="-5" max="5" value="0" autocomplete="off">    
                <span class="legend-min">-5</span>
                <span class="legend-max">5</span>
                <div title="increase" class="control-plus" id="pSteering">+</div>
              </div>
            <div class="title-slider out"> CAMERA <div id="outCamera">0</div> </div>
              <div class="range-box vertical">        
                <div title="Decrease" class="control-minus" id="mCamera">-</div>    
                <input id="cameraRange"  type="range" min="0" max="5" value="0" autocomplete="off">    
                <span class="legend-min">0</span>
                <span class="legend-max">5</span>
                <div title="increase" class="control-plus" id="pCamera">+</div>
              </div>
              
           </div> 
           <div class="button_container box"> 
            <div class="stop_button" id="stopAll">STOP</div>
            <div class="stop_button" id="stopSteering">RESET STEERING</div>
            <div class="stop_button" id="resetCamera">RESET CAMERA</div>
          </div>
        </div>  
      </section>
      <!-- <section>
        <center><h1>Page 2</h1></center>
      </section> -->
  </main>
  <script src="web/assets/jquery-3.6.0.min.js"></script>
  <script src="web/js/main.js"></script>
  <script src="web/js/sliders.js"></script>

</body>
<script>

</script>

</html>

</html>