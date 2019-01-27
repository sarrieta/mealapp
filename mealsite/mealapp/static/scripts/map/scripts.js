function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var map;
function initMap() {

  var locations = [
      ["The Widow's son", 51.5222585, -0.0201964, 6],
      ['Roosters', 51.5246476, -0.0373948, 5],
      ['Greedy Cow', 51.5254043, -0.036794, 4],
      ['Kitchen Pizzeria', 51.5245898, -0.0375992, 3],
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

$(document).ready(function(event){
        $(".view_menu").click( function(event){
          var csrftoken=getCookie('csrftoken')
            var data = {
              restaurant_name_oncard: $('#restaurant_name_oncard').text(),
            }

            $.ajax({
                     type:'POST',
                     url:'/map/',
                     data:data,
                     headers:{
                            "X-CSRFToken": csrftoken
                        },

                     success:function(data){

                       console.log($('#restaurant_name_oncard').text())

                       var items = data.items;
                       for (var i=0;i<items.length;i++) {
                         console.log(items[i].item_name)
                         var item = '<div class="col-md-12 Top">'+ JSON.stringify(items[i].item_name) +'</div>'

                         $('#items_table').append(item);
                       }


						}

                      });
            })

         })
