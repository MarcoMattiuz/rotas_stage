var mapElement = document.getElementById('map');
var loading_map = document.getElementById("loading_map");
var frame = document.getElementById('frame');
var posElement = document.getElementById('pos');
  

var zoom = 18;
var map = null;
var marker = null;
var firstPositionSet = false;

function pos(pos_latitude, pos_longitude, pos_satellites) {
  if (pos_latitude === null || pos_longitude === null ) {
    posElement.classList.add('error-message');
    posElement.innerHTML = 'Impossibile recuperare la posizione';
    return;
  }else{
    var latitude = pos_latitude;
    var longitude = pos_longitude;
    var satellites = pos_satellites;
  
    if (!firstPositionSet) {
      mapElement.innerHTML = '';
      mapElement.style.maxWidth="100%";
      mapElement.style.maxHeight="100%";
      mapElement.style.minWidth="100%";
      mapElement.style.minHeight="100%";

      removeLoading();

      //mappa con prima pos

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
    var newLatLng = new L.LatLng(latitude, longitude);
    marker.setLatLng(newLatLng); 
    posElement.classList.remove('error-message');
    if(satellites==0){
      posElement.innerHTML='Ultima psozione: Latitude: '+latitude+', Longitude: '+longitude;
    }else{
      posElement.innerHTML='Latitude: '+latitude+', Longitude: '+longitude+', Satellites: '+satellites;
    }

    //centrea mappa
    //map.setView([pos_latitude, pos_longitude], zoom);

    marker.on('click', function() {
      map.setView(newLatLng, zoom);
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

  loading_map.classList.remove("d-none");
  mapElement.classList.add("d-none");

  mapElement.classList.remove("leaflet-container")

  posElement.classList.add('error-message');
  posElement.innerHTML = 'Impossibile recuperare la posizione';
}

function removeLoading(){
  loading_map.classList.add("d-none");
  mapElement.classList.remove("d-none");
}