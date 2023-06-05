var mapElement = document.getElementById('map');
var frame = document.getElementById('frame');

var zoom = 18;
var map = null;
var marker = null;
var firstPositionSet = false;

function pos(pos_latitude, pos_longitude, pos_satellites) {
  if (pos_latitude === null || pos_longitude === null ) {
    mapElement.innerHTML = '<div class="error-message">Impossibile recuperare la posizione</div>';
    return;

  }else{

    if (!firstPositionSet) {
      mapElement.innerHTML = '';
    
      //mappa con prima pos
      var latitude = pos_latitude;
      var longitude = pos_longitude;
      var satellites = pos_satellites;

      map = L.map(mapElement).setView([latitude, longitude], zoom);
      marker = L.marker([latitude, longitude], {
        icon: L.icon({
          iconUrl: '../images/icon.png',
          iconSize: [50, 50]
        })
      }).addTo(map);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 30,
        //attribution: 'Mappa dati &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
        attribution:'Latitude: '+latitude+' | Longitude: '+longitude+' | Satellites: '+satellites
      }).addTo(map);

      var satelliteLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 30 ,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        //attribution: 'Mappa dati &copy; <a href="https://www.google.com/maps">Google Maps</a>'
      });

      var baseLayers = {
        'Mappa': L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 30,
          //attribution: 'Mappa dati &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
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
      map.setView(newLatLng, zoom+2);
    });

  }
}

function reset_map() {
  if(map!=null){
    map.remove();
  }
  map = null;
  marker = null;
  firstPositionSet = false;
  mapElement.innerHTML = '<span class="error-message" style="font-size: medium;">Impossibile recuperare la posizione</span>';
}