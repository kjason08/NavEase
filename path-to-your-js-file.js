let map;
let directionsService;
let directionsRenderer;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.5665, lng: 126.9780}, // 대한민국 중심 좌표
    zoom: 7
  });

  directionsService = new google.maps.DirectionsService();
  directionsRenderer = new google.maps.DirectionsRenderer();
  directionsRenderer.setMap(map);
}


function calculateRoute() {
  const start = document.getElementById('start').value;
  const end = document.getElementById('end').value;

  const request = {
    origin: start,
    destination: end,
    travelMode: 'TRANSIT'
  };

  directionsService.route(request, (response, status) => {
    if (status === 'OK') {
      directionsRenderer.setDirections(response);
    } else {
      alert('경로를 찾을 수 없습니다: ' + status);
    }
  });
}
