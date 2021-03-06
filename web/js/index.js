(function() {
  var map = null
  var selectedOrigin = null
  var selectedDestination = null
  var activeLayers = []
  
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

  function initializeMap() {
    // Add here your Mapbox API KEY
    mapboxgl.accessToken = 'API_KEY'
  
    map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/mapbox/light-v9',
      center: [2.09, 41.38],
      zoom: 12,
      hash: true
    })

    map.addControl(new mapboxgl.NavigationControl());

    map.on('load', function() {
      // Ignore
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

  var createGeoJSONCircles = function(path, radiusInKm, points) {
    if(!points) points = 32;

    var features = path.map((pathPiece) => {
      var coords = {
        latitude: pathPiece.lat,
        longitude: pathPiece.lng
      };
  
      var km = radiusInKm;
  
      var ret = [];
      var distanceX = km/(111.320*Math.cos(coords.latitude*Math.PI/180));
      var distanceY = km/110.574;
  
      var theta, x, y;
      for(var i=0; i<points; i++) {
        theta = (i/points)*(2*Math.PI);
        x = distanceX*Math.cos(theta);
        y = distanceY*Math.sin(theta);
  
        ret.push([coords.longitude+x, coords.latitude+y]);
      }
      ret.push(ret[0]);

      return {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates": [ret]
        }
      }
    })
    
    return {
      "type": "geojson",
      "data": {
        "type": "FeatureCollection",
        "features": features
      }
    };
  };

  function searchPath() {
    routingDataAccess.getRoute(selectedOrigin.location, selectedDestination.location)
      .then((routes) => {
        var hasIncident = routes.path.filter((route) => route.path.filter((station) => station.stopid === '1.512').length > 0).length > 0
        
        if (hasIncident)
        {
          $('#avis').show()
          routingDataAccess.updateEdge('1.512', '1.511', 1000)
            .then(() => {
              searchPath()
            })
        }

        var i = 0
        routes.path.forEach((route) => {
          var shape = []
          if (route.shape && route.shape.length > 0 && route.line !== 'T1') {
            route.shape.forEach(singleShape => singleShape.reverse())
            shape = route.shape.reduce((acc, val) => acc.concat(val), [])
          } else {
            shape = route.path
          }
          var layer = {
            "id": route.type + '_' + Math.floor(Math.random() * 1000000),
            "type": "line",
            "source": {
              "type": "geojson",
              "data": {
                "type": "Feature",
                "properties": {
                  "title": ''
                },
                "geometry": {
                  "type": "LineString",
                  "coordinates": shape.map(function(point) {
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
              "line-color": hasIncident ? '#999' : (route.type === 'walk' ? '#888' : lineColor[route.line]),
              "line-width": 3,
              "line-opacity": hasIncident ? 0.5 : 1
            }
          };

          if (route.type === 'walk') {
            layer.paint['line-dasharray'] = [5,3]
          }
          map.addLayer(layer);
          activeLayers.push(layer);

          var circlesLayer = {
            "id": route.line + Math.floor(Math.random() * 1000000),
            "type": 'fill',
            "source": createGeoJSONCircles(route.path, 0.03),
            "paint": {
              "fill-color": hasIncident ? "#999" : "#fff",
              "fill-antialias": true,
              "fill-outline-color": "#000"
            }
          }
          map.addLayer(circlesLayer)
          activeLayers.push(circlesLayer)

          map.addLayer({
            "id": "symbols" + '_' + i,
            "type": "symbol",
            "source": route.type + '_' + i,
            "layout": {
              "symbol-placement": "line",
              "text-font": ["Open Sans Regular"],
              "text-field": '{title}',
              "text-size": 32
            }
          });

          i++
        })
      })
      .catch((err) => {
        // La crida ha fallat
      })
  }

  window.search = function() {
    $('#avis').hide()
    activeLayers.forEach((layer) => {
      map.removeLayer(layer.id)
    })
    activeLayers = []

    searchPath()
  }

  function callGoogleApi(value, callbackName) {
    var key = "API_KEY"; // Add here your API_KEY
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

  $('#avis').hide()

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
