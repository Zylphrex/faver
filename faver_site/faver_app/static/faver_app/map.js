var map;
var default_pos = {lat: 43.663, lng: -79.396};
var $modal = $('.modal').modal({
    show: false
});

$('#request-btn').on('click', function() {
    $modal.modal('show');
});

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: default_pos,
        zoom: 18,
        disableDefaultUI: true,
        heading: 90,
        tilt: 45
    });
}
