(function() {
  var map = null
  var selectedOrigin = null
  var selectedDestination = null

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
    $.get(`https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURI(value)}&key=AIzaSyDF5sfvTf21KwTB2jKrW96PB8qjmmoRidM`)
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
    callGoogleApi(e.target.value, 'onOriginClick')
  })

  $('#inputDestination').on('input', function(e){
    callGoogleApi(e.target.value, 'onDestinationClick')
  })
})();