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

$(function sliderRange() {
    $("#slider-range").slider({
        range: true,
        min: 0,
        max: 50,
        values: [0, 50],
        slide: function( event, ui ) {
      $('#rangeval').html(ui.values[0]+ "£"+ " - "+ui.values[1] + "£");
    }
    });
    var min=$("#range1").val($("#slider-range").slider("values", 0))
    var max =$("#range2").val($("#slider-range").slider("values", 1))


});




   window.onload = function () {

     getCoordinates()
   }

   $(document).ready(function getCoordinates (event){


               $.ajax({
                        type:'GET',
                        url:'/plotMap/',
                        success:function(data){
                          var markers = data

                          LoadMap(markers);
   						}

                         });


            })

   function LoadMap(markers) {
       var mapOptions = {
           center: new google.maps.LatLng(51.5257454,-0.0371079),
           zoom: 8,
           mapTypeId: google.maps.MapTypeId.ROADMAP
       };
       var infoWindow = new google.maps.InfoWindow();
       var latlngbounds = new google.maps.LatLngBounds();
       var map = new google.maps.Map(document.getElementById("map"), mapOptions);

       for (var i = 0; i < markers.coordinates.length; i++) {
           var data = markers.coordinates[i]
           var myLatlng = new google.maps.LatLng(data.lat, data.long);
           var marker = new google.maps.Marker({
               position: myLatlng,
               map: map,
               title: data.name

           });
           (function (marker, data) {
               google.maps.event.addListener(marker, "click", function (e) {
                   infoWindow.setContent("<div style = 'width:200px;min-height:40px'>" + data.name + "</div>");
                   infoWindow.open(map, marker);

               });
           })(marker, data);
           latlngbounds.extend(marker.position);
       }
       var bounds = new google.maps.LatLngBounds();
       map.setCenter(latlngbounds.getCenter());
       map.fitBounds(latlngbounds);
   }



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

   /*var min = document.getElementById('rangevalmin').innerHTML;
   var max = document.getElementById('rangevalmax').innerHTML;
   console.log(min + " hey")
   console.log(max + " hey")*/

   })


$(document).ready(function(event){
        $(".view_menu").click( function getItems(event){


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


          var radios = document.getElementsByName('food_type');
          for (var i = 0, length = radios.length; i < length; i++) {
              if (radios[i].checked) {
                  // do whatever you want with the checked radio

                  radios = radios[i].value

                  break;
              }
          }


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
                        // console.log(items[i].item_name)
                         //var item = '<div class="col-md-12 Top">'+ JSON.stringify(items[i].item_name) +'</div>'
                         var item = '<li class="list-group-item">'+ JSON.stringify(items[i].item_name) +'</li>'

                           list [i]= item
                       }
                       if ( list===" ")
                       {
                         alert("not empty")
                       $('#items_table').html(list);

                     }
                     else{
                       alert('empty')
                       item = "Refine your search parameters"
                       var item = '<li class="list-group-item">'+ JSON.stringify(item) +'</li>'
                       $('#items_table').html(item);

                     }

						}

                      });
            })

         })

/**/


/* allow only one radio to be selected*/

$(document).ready(function(){
    $('input:radio').click(function() {
        $('input:radio').not(this).prop('checked', false);
    });
});
