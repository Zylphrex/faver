var map;
var default_pos = {lat: 43.663, lng: -79.396};
var $reqestModal = $('#request-modal').modal({
    show: false
});

var markers = [];

$(document).ready(function() {
    getRequests();
    var lat = (Math.random() - 0.5) / 10;
    var lng = (Math.random() - 0.5) / 10;

    $('latitude').val(43.663 + lat);
    $('#longitude').val(-79.396 + lat);

    $('#accept-btn').on('click', function() {
        $.ajax({
            url : "/accept-request/",
            type: "POST",
            data : {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'title': $("#details-modal-title").html(),
                'issuer': $("#details-modal-issuer").html(),
            },
            dataType : "json",
            success: function( data ){
                getRequests();
            },
        });
    });

    $('#request-modal').submit(function() {
        $.ajax({
            url : "/post-request/",
            type: "POST",
            data : {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'title': $("#title").val(),
                'description': $("#description").val(),
                'reward': $("#reward").val(),
                'latitude': $("#latitude").val(),
                'longitude': $("#longitude").val()
            },
            dataType : "json",
            success: function( data ){

            },
        });
    });
});

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: default_pos,
        zoom: 18,
        disableDefaultUI: true,
        heading: 90,
        tilt: 45
    });

    map.addListener('dragend', getRequests);
}


function getRequests(){
    $.ajax({url: "/get-requests/",
            type : "GET", // http method

            // handle a successful response
            success : function(json) {
                for (var i = 0; i < markers.length; i++) {
                    markers[i].setMap(null);
                }
                markers = [];

                for (var i = 0; i < json.length; i++) {
                    marker = new google.maps.Marker({
                        position: {
                            lat: parseFloat(json[i]['latitude']),
                            lng: parseFloat(json[i]['longitude'])
                        },
                        map: map,
                        customInfo: {
                            'title': json[i]['title'],
                            'description': json[i]['description'],
                            'issuer': json[i]['issuer'],
                            'reward': json[i]['reward'],
                            'latitude': json[i]['latitude'],
                            'longitude': json[i]['longitude']
                        }
                    });

                    // add click event listeners

                    var markerOnClick = getMarkerOnClick(i);

                    marker.addListener("click", markerOnClick);

                    markers.push(marker);
                }

            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
    });
}

function getMarkerOnClick(i) {

    return Function("$('#details-modal-title').html(markers[" + i + "]['customInfo']['title']);$('#details-modal-description').html(markers[" + i + "]['customInfo']['description']);$('#details-modal-issuer').html(markers[" + i + "]['customInfo']['issuer']);$('#details-modal-reward').html(markers[" + i + "]['customInfo']['reward']);$('#request-details').modal('show');");

}
