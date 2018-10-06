(function() {
  var map = null
  var selectedOrigin = null
  var selectedDestination = null
  
  var routingDataAccess = Koalas.Util.getDataAccess('Routing')
  var metroDataAccess = Koalas.Util.getDataAccess('Metro')

  function initializeMetroStations() {
    metroDataAccess.getMetroStations()
      .then((metroStations) => {
        map.addLayer({
          "id": "points",
          "type": "symbol",
          "source": {
            "type": "geojson",
            "data": {
              "type": "FeatureCollection",
              "features": metroStations.map((metroStation) => {
                return {
                  "type": 'Feature',
                  "geometry": {
                    "type": 'Point',
                    "coordinates": [metroStation.location[1], metroStation.location[0]]
                  },
                  "propeties": {
                    "title": metroStation.name,
                    "icon": "metro"
                  }
                }
              })
            }
          },
          "layout": {
            "icon-image": "{icon}-15",
            "text-field": "{title}",
            "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
            "text-offset": [0, 0.6],
            "text-anchor": "top"
          }
        });
      })
      .catch((err) => {
        // TODO
      })
  }

  function initializeMap() {
    mapboxgl.accessToken = 'pk.eyJ1Ijoia29hbGFzLTIwMTgiLCJhIjoiY2ptd2R6dHI1MDlmMjNrcGpnZnh3Z21lZiJ9.tl5eqrIsTlvZnhE_ceaf4Q'
  
    map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/light-v9',
      center: [2.05, 41.38],
      zoom: 12,
      hash: true
    })

    map.addControl(new mapboxgl.NavigationControl());

    map.on('load', function() {
      initializeMetroStations()

      var origin = [41.376193, 2.121745]
      var destination = [41.371374, 2.099516]
      routingDataAccess.getRoute(origin, destination)
        .then((routes) => {

          var i = 0

          routes.forEach((route) => {
            map.addLayer({
              "id": route.type + '_' + i,
              "type": "line",
              "source": {
                "type": "geojson",
                "data": {
                  "type": "Feature",
                  "properties": {},
                  "geometry": {
                    "type": "LineString",
                    "coordinates": route.path.map(function(coordinate) {
                      return [coordinate[1], coordinate[0]]
                    })
                  }
                }
              },
              "layout": {
                "line-join": "round",
                "line-cap": "round",
              },
              "paint": {
                "line-color": route.type === 'walk' ? '#888' : route.color,
                "line-width": 3
              }
            })

            i++
          })
        })
        .catch((err) => {
          // La crida ha fallat
        })
    })
  }

  window.onOriginClick = function(address) {
    selectedOrigin = {
      name: address.formatted_address,
      location: [address.geometry.location.lat, address.geometry.location.lng]
    }

    $('#inputOrigin')[0].value = selectedOrigin.name
    $('#resultList').html('')
  }

  window.onDestinationClick = function(address) {
    selectedDestination = {
      name: address.formatted_address,
      location: [address.geometry.location.lat, address.geometry.location.lng]
    }

    $('#inputDestination')[0].value = selectedDestination.name
    $('#resultList').html('')
  }

  window.onSearchClick = function() {
    
  }

  function callGoogleApi(value, callbackName) {
    $.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURI(value)}&region=es&key=AIzaSyDF5sfvTf21KwTB2jKrW96PB8qjmmoRidM`)
      .then(results => {
        $('#resultList').html('')
        if (results.status === 'OK') {
          $('#resultList').append(`<a class="mdl-navigation__link" onclick='${callbackName}(${JSON.stringify(results.results[0])})'>${results.results[0].formatted_address}</a>`)
          results.results[0].address_components.forEach(result => {
            $('#resultList').append(`<a class="mdl-navigation__link">${result.long_name}</a>`)
          })
        }
      })
  }

  initializeMap();

  // Gina
  $('#inputOrigin').on('input', function(e){
    if (e.target.value)
      callGoogleApi(e.target.value, 'onOriginClick')
    else
      $('#resultList').html('')
  })

  $('#inputDestination').on('input', function(e){
    if (e.target.value)
      callGoogleApi(e.target.value, 'onDestinationClick')
    else
      $('#resultList').html('')
  })
})();