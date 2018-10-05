(function() {
  var map = null

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

  initializeMap();


  // Gina
  $('#inputOrigin').on('input', function(e){
    console.log(e.target.value)
    $('#resultList').html(e.target.value)
  })

  $('#inputDestination').on('input', function(e){
    console.log(e.target.value)
    $('#resultList').html(e.target.value)
  })

  
})();