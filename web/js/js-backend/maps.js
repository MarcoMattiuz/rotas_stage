var mapElement = document.getElementById('map');
var loading_map = document.getElementById("loading_map");
var frame = document.getElementById('frame');
var posElement = document.getElementById('pos');

var zoom = 16;

var LatLng =null;

var map = null;
var marker = null;
var home = null;

var geoCoordinates = [];
var geoCoordinatesReverse=[];
var newGeoJson = {};

var startCoord = null;
var firstPositionSet = false;
var backHome=0;

function pos(pos_latitude, pos_longitude, pos_satellites) {

  if (pos_latitude === null || pos_longitude === null ){

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

      add_d_none(loading_map);
      remove_d_none(mapElement);

      //mappa con prima pos
      map = L.map(mapElement).setView([longitude,latitude], zoom);

      var baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 30 ,
        //attribution: 'Mappa dati &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors'
      });

      var satelliteLayer = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
        maxZoom: 30 ,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
        //attribution: 'Mappa dati &copy; <a href="https://www.google.com/maps">Google Maps</a>'
      });

      var layersMap = {
        'Mappa': baseLayer,
        'Satellite': satelliteLayer
      };


      L.control.layers(layersMap).addTo(map);
      map.addLayer(satelliteLayer);
      
      marker = L.marker([longitude,latitude], {
        icon: L.icon({
          iconUrl: '../images/icon.png',
          iconSize: [50, 50]
        })
      }).addTo(map);

      firstPositionSet=true;
    }

    if(startCoord == null){

      startCoord=[longitude,latitude];
      home = L.marker(startCoord, {
        icon: L.icon({
          iconUrl: '../images/home.png',
          iconSize: [40, 40]
        })
      }).addTo(map);
      
    }
    
    //aggiorna marker
    LatLng = new L.LatLng(longitude, latitude);
    marker.setLatLng(LatLng); 
    
    //polyline -> tutte le posizoni del marker 
    polyline([latitude, longitude]);

    if(startCoord[0] === latitude && startCoord[1] === longitude){
      backHome++;
    }

    if(backHome%2==0){
      geoCoordinatesReverse=geoCoordinates;
      for (let i = 0; i < geoCoordinatesReverse.length; i++) {
        let temp = geoCoordinatesReverse[i][0];
        geoCoordinatesReverse[i][0] = geoCoordinatesReverse[i][1];
        geoCoordinatesReverse[i][1] = temp;
      }

      var polygon = L.polygon(geoCoordinatesReverse, {color: '#ff7800'});

      geoCoordinates=geoCoordinatesReverse;
      for (let i = 0; i < geoCoordinates.length; i++) {
        let temp = geoCoordinates[i][0];
        geoCoordinates[i][0] = geoCoordinates[i][1];
        geoCoordinates[i][1] = temp;
      }

      polygon.addTo(map);

      home.remove();
    }else{
      home.addTo(map);
    }
    

    //map.setView(LatLng, zoom);
    
    marker.on('click', function() {
      map.setView(LatLng, zoom);
    });
    home.on('click', function() {
      map.setView(startCoord, zoom);
    });

    posElement.classList.remove('error-message');
    if(satellites==0){
      posElement.innerHTML='Ultima psozione: Latitude: '+latitude+', Longitude: '+longitude;
    }else{
      posElement.innerHTML='Latitude: '+latitude+', Longitude: '+longitude+', Satellites: '+satellites;
    }
  }
}


function polyline(coord){
  geoCoordinates.push(coord);

  newGeoJson = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "properties": {},
        "geometry": {
          "coordinates": geoCoordinates,
          "type": "LineString"
        },
        "id": 0
      }
    ]
  };

  var style = {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.6
  };

  L.geoJSON(newGeoJson, {style: style}).addTo(map);
}

function reset_map() {
  firstPositionSet=false;
  if(map!=null){
    map.remove();
  }

  map = null;
  marker = null;
  home = null;
  LatLng =null;
  geoCoordinates = [];
  geoCoordinatesReverse=[];
  newGeoJson = {};
  startCoord = null;

  //remove_d_none(loading_map);
  //add_d_none(mapElement);

  mapElement.classList.remove("leaflet-container")

  posElement.classList.add('error-message');
  posElement.innerHTML = 'Impossibile recuperare la posizione';
}
