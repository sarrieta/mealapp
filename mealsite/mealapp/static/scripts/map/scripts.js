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


var markers = [
   {
       "title": 'Kilikya Mile End',
       "lat": '51.5280916',
       "lng": '-0.0408652',
       "description": 'We serve healthy, authentic, good quality Turkish food. We offer a choice of beverages including; various teas and coffees. Kilikya is also a Halal restaurant.'
   },
   {
       "title": 'The Widows Son',
       "lat": '51.5222618',
       "lng": '-0.0181499',
       "description": 'We serve; unusual infusion based cocktails, a mixture of delicious burgers, merged with the classic east end boozer featuring variety of draught beers & bottles'
   },
   {
       "title": 'Palmers',
       "lat": '51.5300426',
       "lng": '-0.0430964',
       "description": "We are a family run restaurant (father and son's) and have been in the business all our lives. Our aim is to satisfy our customers with great food and wine with fantastic value, a warm and friendly service as it should be in a family restaurant"
   },
   {
       "title": 'Sultan',
       "lat": '51.5341287',
       "lng": '-0.0267071',
       "description": 'We are a small family run restaurant who and we invite you to try and love our variety of grills, soups , breads and salads.'
   },
   {
       "title": '90 Degrees',
       "lat": '51.5222929',
       "lng": '-0.0449038',
       "description": 'At 90° MELT, we have a massive passion for simple, but wholesome comfort food and we are constantly bringing vegan and veggie versions – so all the good bits of American Comfort food, sustainably and responsibly.'
   },
   {
       "title": 'Verdi',
       "lat": '51.5222774',
       "lng": '-0.0447649',
       "description": " Named after Parma's most famous son and foodie, we warmly welcome guests into our beautiful family run restaurant, where the focus is on simple yet authentic Italian cuisine.  "
   },
   {
       "title": 'Bacaro',
       "lat": '51.5314448',
       "lng": '-0.0380137',
       "description": 'Bacaro is constantly looking to bring new and exciting dishes to your table, is uniquely designed around seasonal produce from carefully selected suppliers and artisan producers across Italy and the UK. '
   }
 ];

   window.onload = function () {
       LoadMap();
   }
   function LoadMap() {

     $.getJSON("data.json", function(json) {
         //console.log(json);
         alert(json); // this will show the info it in firebug console
     });
       var mapOptions = {
           center: new google.maps.LatLng(51.5257454,-0.0371079),
           zoom: 8,
           mapTypeId: google.maps.MapTypeId.ROADMAP
       };
       var infoWindow = new google.maps.InfoWindow();
       var latlngbounds = new google.maps.LatLngBounds();
       var map = new google.maps.Map(document.getElementById("map"), mapOptions);

       for (var i = 0; i < markers.length; i++) {
           var data = markers[i]
           var myLatlng = new google.maps.LatLng(data.lat, data.lng);
           var marker = new google.maps.Marker({
               position: myLatlng,
               map: map,
               title: data.title
           });
           (function (marker, data) {
               google.maps.event.addListener(marker, "click", function (e) {
                   infoWindow.setContent("<div style = 'width:200px;min-height:40px'>" + data.description + "</div>");
                   infoWindow.open(map, marker);

               });
           })(marker, data);
           latlngbounds.extend(marker.position);
       }
       var bounds = new google.maps.LatLngBounds();
       map.setCenter(latlngbounds.getCenter());
       map.fitBounds(latlngbounds);
   }

   var min;

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
                       $('#items_table').html(list);


						}

                      });
            })

         })

/* allow only one radio to be selected*/

$(document).ready(function(){
    $('input:radio').click(function() {
        $('input:radio').not(this).prop('checked', false);
    });
});
