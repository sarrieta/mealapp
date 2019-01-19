
var map;
function initMap() {

  var locations = [
      ['Roosters', 51.5246476, -0.0373948, 4],
      ['Greedy Cow', 51.5254043, -0.036794, 5],
      ['Kitchen Pizzeria', 51.5245898, -0.0375992, 3],
      ['Nandos', 51.522451, -0.0542593, 2],
      ['Kilikya Mile End', 51.5280883, -0.0429117, 1]
    ];

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 51.520497918, lng: -0.03749985},
        zoom: 14
      });

    var infowindow = new google.maps.InfoWindow();

    var marker, i;

    for (i = 0; i < locations.length; i++) {
      marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map
      });

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infowindow.setContent(locations[i][0]);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
}
