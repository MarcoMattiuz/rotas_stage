// sendData.js
var websocket;

function sendMessage(message) {
  // msg inviare al WebSocket
  if (message != undefined) {
    websocket.send(message);
  }
}