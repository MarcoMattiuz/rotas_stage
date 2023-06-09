var videoData = []

window.player = new Player({ 
    useWorker: true, 
    // workerFile: 'js/js-frontend/video/Decoder.js',
    webgl: 'auto', 
    size: { width: 848, height: 480 } 
});

var playerElement = document.getElementById('viewer');

function player_decode(data){
    console.log("window: "+window);
    console.log("data: "+data);
    
    videoData.push(data)

    window.player.decode(new Uint8Array(videoData));
    
    playerElement.appendChild(window.player.canvas);

}



/*
var video = new Broadway.Player({ useWorker: true });

video.onPictureDecoded = function (buffer, width, height) {
  canvas.width = width;
  canvas.height = height;
  var imageData = ctx.createImageData(width, height);
  imageData.data.set(buffer);
  ctx.putImageData(imageData, 0, 0);
};
function handleVideoData(data) {
  var uint8Array = new Uint8Array(data);
  video.decode(uint8Array);
}*/

    