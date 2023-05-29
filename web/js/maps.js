var mapElement = document.getElementById('map');
var zoom = 1;
var map = null;
var marker = null;

function pos(pos_latitude, pos_longitude) {
  if (map) {
    // Aggiorna la posizione del marker
    marker.setLatLng([pos_latitude, pos_longitude]);
    
    // Centra la mappa alle nuove posizioni
    map.setView([pos_latitude, pos_longitude], zoom);
  } else {
    // Crea la mappa con le posizioni iniziali
    latitude = pos_latitude;
    longitude = pos_longitude;
    map = L.map(mapElement).setView([latitude, longitude], zoom);
    
    marker = L.marker([latitude, longitude], {
      icon: L.icon({
        iconUrl: '../images/icon.png',
        iconSize: [50, 50]
      })
    }).addTo(map);
    
    marker.on('click', function () {
      map.setView(marker.getLatLng(), zoom);
    });
    
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
  }
}
