(function() {
  var map = null
  var selectedOrigin = null
  var selectedDestination = null
  
  var routingDataAccess = Koalas.Util.getDataAccess('Routing')
  var metroDataAccess = Koalas.Util.getDataAccess('Metro')

  var lineColor = {
    'L1': '#CB2508',
    'L2': '#90278E',
    'L3': '#067634',
    'L4': '#FFC10D',
    'L5': '#006B9D',
    'L9S': '#DF8D33',
    'T1': '#0C7557',
    'T2': '#0C7557',
    'T3': '#0C7557'
  }

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
    })
  }

  window.onOriginClick = function(name, lat, lng) {
    selectedOrigin = {
      name: name,
      location: [lat, lng]
    }

    $('#inputOrigin')[0].value = selectedOrigin.name
    $('#resultList').html('')
  }

  window.onDestinationClick = function(name, lat, lng) {
    selectedDestination = {
      name: name,
      location: [lat, lng]
    }

    $('#inputDestination')[0].value = selectedDestination.name
    $('#resultList').html('')
  }

  window.search = function() {
    routingDataAccess.getRoute(selectedOrigin.location, selectedDestination.location)
      .then((routes) => {
        console.log(routes)
        var i = 0
        routes.path.forEach((route) => {
          var layer = {
            "id": route.type + '_' + i,
            "type": "line",
            "source": {
              "type": "geojson",
              "data": {
                "type": "Feature",
                "properties": {},
                "geometry": {
                  "type": "LineString",
                  "coordinates": route.path.map(function(point) {
                    return [point.lng, point.lat]
                  })
                }
              }
            },
            "layout": {
              "line-join": "round",
              "line-cap": "round",
              
            },
            "paint": {
              "line-color": route.type === 'walk' ? '#888' : lineColor[route.line],
              "line-width": 3
            }
          };

          if (route.type === 'walk') {
            layer.paint['line-dasharray'] = [5,3]
          }
          map.addLayer(layer)

          i++
        })
      })
      .catch((err) => {
        // La crida ha fallat
      })
  }

  function callGoogleApi(value, callbackName) {
    var key = "AIzaSyDF5sfvTf21KwTB2jKrW96PB8qjmmoRidM"; // Add here your API_KEY
    $.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURI(value)}&region=es&key=${key}`)
      .then(results => {
        $('#resultList').html('')
        if (results.status === 'OK') {
          $('#resultList').append(`<a class="mdl-navigation__link" onclick='${callbackName}("${results.results[0].formatted_address}", ${results.results[0].geometry.location.lat}, ${results.results[0].geometry.location.lng})'>${results.results[0].formatted_address}</a>`)
          results.results[0].address_components.forEach(result => {
            $('#resultList').append(`<a class="mdl-navigation__link">${result.long_name}</a>`)
          })
        }
      })
  }

  initializeMap();

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