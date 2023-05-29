var mapElement = document.getElementById('map');
var zoom = 15;
var map = null;
var marker = null;
var firstPositionSet = false;

function pos(pos_latitude, pos_longitude) {
  if (pos_latitude === null || pos_longitude === null) {
    // Coordinate nulle, mostra messaggio di errore sulla mappa
    mapElement.style.background = "#f8f8f8";
    mapElement.style.display = "flex";
    mapElement.style.justifyContent = "center";
    mapElement.style.alignItems = "center";
    mapElement.style.fontSize = "24px";
    mapElement.style.color = "#555";
    mapElement.innerHTML = '<div class="error-message">Impossibile recuperare la posizione.</div>';
    return;
  }else{

    if (!firstPositionSet) {
      mapElement.innerHTML = '';
    
      //mappa con prima pos
      var latitude = pos_latitude;
      var longitude = pos_longitude;
      map = L.map(mapElement).setView([latitude, longitude], zoom);
      marker = L.marker([latitude, longitude], {
        icon: L.icon({
          iconUrl: '../images/icon.png',
          iconSize: [50, 50]
        })
      }).addTo(map);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 30,
        attribution: 'Mappa dati &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      }).addTo(map);

      var satelliteLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 30,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        attribution: 'Mappa dati &copy; <a href="https://www.google.com/maps">Google Maps</a>'
      });

      var baseLayers = {
        'Mappa': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: 'Mappa dati &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        }),
        'Satellite': satelliteLayer
      };

      L.control.layers(baseLayers).addTo(map);
      map.addLayer(satelliteLayer);

      firstPositionSet = true;
    }

    //aggiorna marker
    var newLatLng = new L.LatLng(pos_latitude, pos_longitude);
    marker.setLatLng(newLatLng); 

    //centrea maooa
    //map.setView([pos_latitude, pos_longitude], zoom);
    
    marker.on('click', function() {
      map.setView(newLatLng, zoom+5);
    });
  }
}

function toggleFullscreen() {
  if (!document.fullscreenElement) {
    if (mapElement.requestFullscreen) {
      mapElement.requestFullscreen();
    } else if (mapElement.mozRequestFullScreen) {
      mapElement.mozRequestFullScreen();
    } else if (mapElement.webkitRequestFullscreen) {
      mapElement.webkitRequestFullscreen();
    } else if (mapElement.msRequestFullscreen) {
      mapElement.msRequestFullscreen();
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  }
}