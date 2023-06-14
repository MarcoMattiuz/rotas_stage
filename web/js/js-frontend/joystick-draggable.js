var toggleButton = document.getElementsByClassName('toggle-joystick'); // Bottone per aprire e chiudere il joystick
var div = document.getElementById('joystick-draggable');
var dragOverlay = document.getElementById('drag-overlay');
var navToggler = document.getElementById('nav-toggler');
var startX = 0, startY = 0, startRight = 0, startBottom = 0;
var posx=0 ,posy=0;
var dragging = false;
var manager;
div.style.display = 'none';
dragOverlay.style.display = 'none';




for (var i = 0; i < toggleButton.length; i++) {
    toggleButton[i].addEventListener('click', function() {
        if (connect && !controllerConnect) {
            if (div.style.display === 'none') {
                openJoy();
                div.style.display = 'block';
                dragOverlay.style.display = 'block';
                posx=parseInt(window.getComputedStyle(div).right);
                posy=parseInt(window.getComputedStyle(div).bottom);
            } else {
                destroyDivJoystick();
            }
        }
    });
}

navToggler.addEventListener('click', function() {
    if (connect && !controllerConnect) {
        var navTogglerAttribute = document.getElementById('nav-toggler').getAttribute('aria-expanded');
        setTimeout(function() {
            if (manager) {
                updateJoystick();
            }
        }, 500);
    }
});

div.addEventListener('mousedown', handleDragStart);
div.addEventListener('touchstart', handleDragStart);

function handleDragStart(event) {
    if ((event.target === dragOverlay) && connect) {
        startX = getEventX(event);
        startY = getEventY(event);
        startRight = parseInt(window.getComputedStyle(div).right);
        startBottom = parseInt(window.getComputedStyle(div).bottom);
        dragging = true;
    }
}

document.addEventListener('mousemove', handleDragMove);
document.addEventListener('touchmove', handleDragMove);

function handleDragMove(event) {
    if (dragging && connect && !controllerConnect) {
        event.preventDefault();
        var newRight = startRight + startX - getEventX(event);
        var newBottom = startBottom + startY - getEventY(event);
        div.style.right = newRight + 'px';
        div.style.bottom = newBottom + 'px';
    }
}

document.addEventListener('mouseup', handleDragEnd);
document.addEventListener('touchend', handleDragEnd);

function handleDragEnd(event) {
    if (connect && !controllerConnect) {
        if (manager) {
            updateJoystick();
        }
        dragging = false;
    }
}

function destroyDivJoystick() {
    div.style.display = 'none';
    dragOverlay.style.display = 'none';
    div.style.right = posx + 'px';
    div.style.bottom = posy + 'px';
}

function getEventX(event) {
    if (event.touches && event.touches.length > 0) {
        return event.touches[0].clientX;
    } else {
        return event.clientX;
    }
}

function getEventY(event) {
    if (event.touches && event.touches.length > 0) {
        return event.touches[0].clientY;
    } else {
        return event.clientY;
    }
}
