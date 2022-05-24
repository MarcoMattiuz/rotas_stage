window.addEventListener("load", () => { eel.start() }, false); //quando il programma si starta

eel.expose(prompt_alerts);
function prompt_alerts(description) {
  alert(description);
}