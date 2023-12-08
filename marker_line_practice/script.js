
// Function to load marker data from an external JSON file
function loadMarkerData(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                callback(JSON.parse(xhr.responseText));
            } else {
                console.error('Failed to load marker data');
            }
        }
    };
    xhr.open('GET', url, true);
    xhr.send();
}

function initMap() {
    // Specify the center of the map
    var center = {lat: 36.361862, lng: 127.337170};

    // Creating a new map
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: center
    });

    // Load marker data from an external file
    loadMarkerData('./kjason08.github.io/Markers.markers.json', function(markers) {
        // Creating an array to hold the Google Maps LatLng objects
        var latLngs = [];

        // Creating LatLng objects from the marker data (markers not displayed on the map)
        markers.forEach(function(markerData) {
            var latLng = new google.maps.LatLng(markerData.lat, markerData.lng);
            latLngs[markerData.number] = latLng;
        });

        // Function to draw a line between specified markers
        function connectMarkers(markerIndices) {
            var coordinates = markerIndices.map(function(index) {
                return latLngs[index];
            });

            var path = new google.maps.Polyline({
                path: coordinates,
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2
            });

            path.setMap(map);
        }

        // Connect specified markers (Example: 1, 4, 22, 111)
        connectMarkers([1, 4, 22, 111]);
    });
}
