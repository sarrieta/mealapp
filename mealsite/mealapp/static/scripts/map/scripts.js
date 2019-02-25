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

function calcDistance (fromLat, fromLng, toLat, toLng) {
      return google.maps.geometry.spherical.computeDistanceBetween(
        new google.maps.LatLng(fromLat, fromLng), new google.maps.LatLng(toLat, toLng));
   }


   window.onload = function () {

     getCoordinates()


   }


   function getCoordinates (event){
               $.ajax({
                        type:'GET',
                        url:'/plotMap/',
                        success:function(data){
                          var markers = data

                          LoadMap(markers);
   						}
                         });

            }

   function LoadMap(markers) {



     if (navigator.geolocation) {


       navigator.geolocation.getCurrentPosition(function(position) {

         var pos = {
           lat: position.coords.latitude,
           lng: position.coords.longitude
         };
         var mapOptions = {
             center: new google.maps.LatLng(pos.lat,pos.lng),
             zoom: 13,
             mapTypeId: google.maps.MapTypeId.ROADMAP
         };

         var infoWindow = new google.maps.InfoWindow();
         var latlngbounds = new google.maps.LatLngBounds();
         var map = new google.maps.Map(document.getElementById("map"), mapOptions);


         val='limit'
         radius = radioVal(val)



         if (radius)
         {

           limit = radius;

         }
         else{
         limit = 5;

          }
          circleRadius= limit * 1000
          var circle = new google.maps.Circle({
             map: map,
             radius: circleRadius,    // 10 miles in metres
             center: new google.maps.LatLng(pos.lat,pos.lng) ,
             fillColor: '#AA0000'
           });

         for (var i = 0; i < markers.coordinates.length; i++) {
             var data = markers.coordinates[i]
             var myLatlng = new google.maps.LatLng(data.lat, data.long);


            var radius = parseInt(limit, 10)*1000;


            var d = calcDistance(data.lat,data.long,pos.lat,pos.lng)


            if (d<=radius){


              var marker = new google.maps.Marker({
                  position: myLatlng,
                  map: map,
                  title: data.name

              });
              (function (marker, data) {
                  google.maps.event.addListener(marker, "click", function (e) {
                       e.preventDefault();
                      infoWindow.setContent("<div style = 'width:200px;min-height:40px'>" + data.name + "</div>");
                      infoWindow.open(map, marker);

                  });
              })(marker, data);
              latlngbounds.extend(marker.position);

            }

         }

         initMap(map)

       });

     }

    else{

      console.log('no location')
    }


   }

   $(document).ready(function() {
    $('input:radio[name=limit]').change(function() {
        if (this.value == '1') {
              radius=1;
            //  alert(radius)
             getCoordinates(radius)
        }
        else if (this.value == '5') {
              radius=5;
              //alert(radius)
             getCoordinates(radius)
        }
        else if (this.value == '10') {
            radius=10;
            //alert(radius)
             getCoordinates(radius)
        }
        else {
            radius=15;
            //alert(radius)
             getCoordinates(radius)
        }


    });
});

   function radioVal(val){

     var radios = document.getElementsByName(val);
         for (var i = 0, length = radios.length; i < length; i++) {
             if (radios[i].checked) {

                 radios = radios[i].value

                 return radios;

                 break;
             }
         }

   }

   function initMap(map) {

     var directionsDisplay = new google.maps.DirectionsRenderer;
     var directionsService = new google.maps.DirectionsService;

     directionsDisplay.setMap(map);
     directionsDisplay.setPanel(document.getElementById('right-panel'));

     var control = document.getElementById('floating-panel');
     control.style.display = 'block';
     map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);

     var onChangeHandler = function() {
       calculateAndDisplayRoute(directionsService, directionsDisplay);
     };
     //document.getElementById('start').addEventListener('change', onChangeHandler);
     document.getElementById('end').addEventListener('change', onChangeHandler);
   }


   function calculateAndDisplayRoute(directionsService, directionsDisplay) {

       if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
              var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
              };

              var geocoder = new google.maps.Geocoder;

              var latlng = {lat: parseFloat(pos.lat), lng: parseFloat(pos.lng)};

              geocoder.geocode({'location': latlng}, function(results, status) {
                if (status === 'OK') {
                  if (results[0]) {
                    //console.log('in in if')
                    currenLoc= results[0].formatted_address;

                      var start = currenLoc

                      var end = document.getElementById('end').value;

                      directionsService.route({
                        origin: start,
                        destination: end,
                        travelMode: 'DRIVING'
                      }, function(response, status) {
                        if (status === 'OK') {
                          directionsDisplay.setDirections(response);
                        } else {
                          window.alert('Directions request failed due to ' + status);
                        }
                      });

                  } else {
                    window.alert('No results found');
                  }
                } else {
                  window.alert('Geocoder failed due to: ' + status);
                }
              });

            }, function() {
              handleLocationError(true, infoWindow, map.getCenter());
            });
          } else {
            // Browser doesn't support Geolocation
            handleLocationError(false, infoWindow, map.getCenter());


          }


        function handleLocationError(browserHasGeolocation, infoWindow, pos) {
          infoWindow.setPosition(pos);
          infoWindow.setContent(browserHasGeolocation ?
                                'Error: The Geolocation service failed.' :
                                'Error: Your browser doesn\'t support geolocation.');
          infoWindow.open(map);
        }


   }
   $(".reset").click( function getDirections(event){


     getCoordinates()



   })





$(document).ready(function(event){
   $("#slider-range").slider({
       range: true,
       min: 0,
       max: 40,
       animate: true,
       step: 0.5,
       values: [0, 40],
       slide: function( event, ui ) {
             $('#rangevalmin').html(ui.values[0]+ " £ -");
             $('#rangevalmax').html(" " +ui.values[1] + " £");
           },
       stop: function( event, ui ) {
       min = ui.values[0];
       max = ui.values[1];
       //console.log(min + " hey")
       //console.log(max + " hey")
       $("#minValue").val(min)
       $("#maxValue").val(max)

     }
   });

   })


$(document).ready(function(event){
        //$(".view_menu").click( function getItems(event){
        $(".view_menu").on("click", function getItems(event){



          var id = $(this).parent().attr('id');

          min=$("#minValue").val()
          max=$("#maxValue").val()

          if( min.length==0 || max.length==0)
          {
            min=0
            max=40
          }
          else{
            min=min
            max=max

          }

          var radios =radioVal('food_type')
          var csrftoken=getCookie('csrftoken')


            $.ajax({
                     type:'POST',
                     url:'/map/',
                     data:{'id': id, 'food_type':radios,'min':min,'max':max },
                     headers:{
                            "X-CSRFToken": csrftoken
                        },

                     success:function(data){

                       var list = new Array()

                       var items = data.items;


                       for (var i=0;i<items.length;i++) {
                         name = JSON.stringify(items[i].item_name)
                         pName= name.replace(/['"]+/g, '');

                         desc = JSON.stringify(items[i].item_description)
                         pDesc= desc.replace(/['"]+/g, '');

                         price = JSON.stringify(items[i].item_price)
                         pPrice= price.replace(/['"]+/g, '');


                           var $tr = $('<tr/>');
                            $tr.append($('<td scope="col" style="color:black"/>').text(pName));
                            $tr.append($('<td scope="col" style="color:black"/>').text(pDesc));
                            $tr.append($('<td scope="col" style="color:black"/>').text(pPrice));

                            $('.table-wrapper-scroll-y tr:last').after($tr);
                              }
                        }

                   });
         })

  });

    $(document).ready(function(){
      $(function () {
    var firstTime = true;

    $("#myselction").change(function (e) {
        var neData = $("#myselction").val();

        if (firstTime) {
            $("table.data thead tr").append("<th>Idea</th>");
            $("table.data tr:gt(0)").append("<td>" + neData + "</td>");
            firstTime = false;
        } else {
            $("table.data tr:gt(0) td:last-child").html(neData);
        }
    });
});

        });


  $(document).ready(function(){
/*
    var $rows = $('#myTable tr');
      $('#search').keyup(function() {
        var val = $.trim($(this).val()).replace(/ +/g, ' ').toLowerCase();

        $rows.show().filter(function() {
            var text = $(this).text().replace(/\s+/g, ' ').toLowerCase();
            return !~text.indexOf(val);
        }).hide();
      });*/
  });





$(document).ready(function(){
    $('input:radio').click(function() {
        $('input:radio').not(this).prop('checked', false);
    });
});
