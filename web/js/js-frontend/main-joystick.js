var toggleButton = document.getElementById('toggle-joystick'); // Bottone per aprire e chiudere il joystick
var controller = document.getElementById('joystick'); // Div contenente il joystick

controller.style.display = 'none';


toggleButton.addEventListener('click', function() {
    if(connect&&!controllerConnect){
        controller = document.getElementById('joystick');
        if (!manager) 
        {
            createJoystick();
            listenJoystick();
        }
        else 
        {
            destroyJoystick();
        }
    }
});

function createJoystick(){
    controller.style.display = 'block';
    manager = nipplejs.create({
        zone: controller,
        color: '#ff0000',
        size: 100,
        mode: 'static',
        position: { top: '50%', left: '50%' }
    });
}

function listenJoystick(){
    manager.on('start', function (event, nipple) {
        nipple.on('move', function (event, data) {
            var x = Math.round(-data.vector.x * 1023); 
            var y = Math.round(data.vector.y * 1023);
            
            x = Math.max(Math.min(x, 1023), -1023);
            y = Math.max(Math.min(y, 1023), -1023);

            setStearing(x, y);
        });
    });
    
}

function destroyJoystick()
{
    controller.style.display = 'none';
    manager.destroy();
    manager = null;
}

function updateJoystick()
{
    destroyJoystick();
    createJoystick();
    listenJoystick();
}   