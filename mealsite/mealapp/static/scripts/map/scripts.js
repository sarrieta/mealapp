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
     getRestaurants()


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
         limit = 3;

          }
          circleRadius= limit * 1000
          var circle = new google.maps.Circle({
             map: map,
             radius: circleRadius,    // 10 miles in metres
             center: new google.maps.LatLng(pos.lat,pos.lng) ,
             //fillColor: '#AA0000',
            // strokeColor: '#FF0000',
             strokeOpacity: 0.8,
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
        getCoordinates()

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



        //$(".view_menu").click( function getItems(event){
        $(document).on('click', '.view_menu', function getItems(event){



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
          var cuisine =radioVal('cuisine')

          var csrftoken=getCookie('csrftoken')


            $.ajax({
                     type:'POST',
                     url:'/map/',
                     data:{'id': id, 'food_type':radios,'min':min,'max':max, 'cuisine':cuisine },
                     headers:{
                            "X-CSRFToken": csrftoken
                        },

                     success:function(data){

                       var list = new Array()

                       var items = data.items;

                       $("#item_list").empty()

                       for (var i=0;i<items.length;i++) {
                         name = JSON.stringify(items[i].item_name)
                         pName= name.replace(/['"]+/g, '');

                         desc = JSON.stringify(items[i].item_description)
                         pDesc= desc.replace(/['"]+/g, '');

                         price = JSON.stringify(items[i].item_price)
                         pPrice= price.replace(/['"]+/g, '');



                            /*$("#item_list").append("<li style='color:black;text-align:left' ><a data-toggle='tab'>" + pName + ' '+ pDesc + ' ' + pPrice +'£'
                            + " </a></li>");*/

                            demo =i;

                            $("#item_list").append("<li id='"+pName+"'style='color:black;text-align:left'><a> <button name='john' type='button' class='btn btn-info' data-toggle='collapse' data-target=#" + demo +">" + pName + '</button>' + '</a>' + "<button id='addSummary' value='"+pName+"' name='"+pPrice+"' type='button' class='btn-xs'> Add </button></li><br>");
                            $("#item_list").append("<div id='"+ demo+ "' class='collapse' style='color:black;text-align:left'>" + pDesc + ' ' + pPrice+ "</div> </li>");
                            //$("#item_list").append("<li class='summaryInfo'style='display:none;'><a>" + pName + '</a>' + "</li><br>");


                              }
                        }

                   });


  });

  function myFunctionX() {

      var sum=0;

      var x = document.getElementsByClassName("totalPrice");
      var i;
      for (i = 0; i < x.length; i++) {
        total = x[i].innerHTML

        sum = parseFloat(sum) + parseFloat(total)

      }
      console.log(sum)
      $("#spanCart span").text('Total:' + ' ' +sum + ' ' + '£');
  }

  $(document).on('click', '#addSummary', function getItems(event){

    name = $(this).val();//if you are trying to get value of 'value' attribute
    price =$(this).attr('name');

/*
    var $tds = $('#modal_cart tr > td:nth-child(2)').filter(function () {
    return $.trim($(this).text()) == VALUE;
    });
    if ($tds.length != 0) {
        alert("Please enter a unique row number.");
    }*/
    var total=0;

    $('#modal_cart tbody').append('<tr><td>'+ name +'</td><td class="totalPrice">'+ price +'</td><td><a><i class="fas fa-times"></i></a></td></tr>');

    myFunctionX();




      });



/*$( "#cartInput" ).keyup(function() {
  alert( "Handler for .keyup() called." );
});*/

$(document).ready(function(){
$("input").click(function(){
        $(this).next().show();
        $(this).next().hide();
    });

});







        function getRestaurants (event){
                  $.ajax({
                           type:'GET',
                           url:'/plotMap/',
                           success:function(data){
                             var markers = data



                          for (var i = 0; i < markers.coordinates.length; i++) {
                                 var data = markers.coordinates[i]


                               $("#rest_list").append("<li class='list-group-item'><a>"+
                               "<div id='" + data.id + "' class='iden'>" +
                               "<h4 class='card-title'>"+ data.name +"</h4>"+
                               "<br>"+
                               "<h6 class='card-subtitle mb-2 text-muted'>"+ data.opening +"</h6>"+
                               "<p class='card-text'> </p>"+
                               "<button id='menu_button' class='view_menu'>View Menu</button>"+ "</div>"
                                +" </a></li><br>");


                             }


      						}
                            });

               }





/*$(document).ready(function(){
    $('input:radio').click(function() {
        $('input:radio').not(this).prop('checked', false);
    });
});*/
