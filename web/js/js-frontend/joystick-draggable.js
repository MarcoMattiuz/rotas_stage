var toggleButton = document.getElementById('toggle-joystick'); // Bottone per aprire e chiudere il joystick
var div = document.getElementById('joystick-draggable');
var dragOverlay = document.getElementById('drag-overlay');
var navToggler = document.getElementById('nav-toggler');
var startX = 0, startY = 0, startRight = 0, startBottom = 0;
var dragging = false;
var manager;
div.style.display = 'none';
dragOverlay.style.display = 'none';

toggleButton.addEventListener('click', function() {
    if(connect&&!controllerConnect){
        if (div.style.display === 'none') 
        {   
            div.style.display = 'block';
            dragOverlay.style.display = 'block';
            
        }
        else 
        {
            destroyDivJoystick();
        }
    }
});

navToggler.addEventListener('click', function() {
    if(connect&&!controllerConnect){
        var navTogglerAttribute = document.getElementById('nav-toggler').getAttribute('aria-expanded');
        
        if (navTogglerAttribute === 'false')
        {
            setTimeout(function() {if(manager){updateJoystick();}}, 500);
        }
        else{
            setTimeout(function() {if(manager){updateJoystick();}}, 500);
        }
    }
});
    
    
div.addEventListener('mousedown', function (e) {
    if ((e.target === dragOverlay)&&connect) 
    {
        startX = e.clientX;
        startY = e.clientY;
        startRight = parseInt(window.getComputedStyle(div).right);
        startBottom = parseInt(window.getComputedStyle(div).bottom);
        dragging = true;
                
    }
});

document.addEventListener('mousemove', function (e) {
    if (dragging&&connect&&!controllerConnect) 
    {
        var newRight = startRight + startX - e.clientX;
        var newBottom = startBottom + startY - e.clientY;
        div.style.right = newRight + 'px';
        div.style.bottom = newBottom + 'px';
    }

});

document.addEventListener('mouseup', function (e) {
    if(connect&&!controllerConnect){
        if(manager){updateJoystick();} 
        dragging = false;
    }
});

function destroyDivJoystick(){
    div.style.display = 'none';
    dragOverlay.style.display = 'none';
}