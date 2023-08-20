<!DOCTYPE html>
<html>
<head>
  <title>경로 탐색 예제</title>
  <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"></script>
</head>
<body>
  <div>
    <label for="start">출발지:</label>
    <input type="text" id="start" placeholder="출발지 주소">
    <br>
    <label for="end">도착지:</label>
    <input type="text" id="end" placeholder="도착지 주소">
    <br>
    <button onclick="calculateRoute()">경로 탐색</button>
  </div>
  <div id="map" style="height: 400px;"></div>

  <script>
    let map;
    let directionsService;
    let directionsRenderer;

    function initMap() {
      map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7749, lng: -122.4194}, // San Francisco 좌표
        zoom: 13
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
        travelMode: google.maps.TravelMode.DRIVING
      };

      directionsService.route(request, function(response, status) {
        if (status === 'OK') {
          directionsRenderer.setDirections(response);
        } else {
          alert('경로를 찾을 수 없습니다: ' + status);
        }
      });
    }
  </script>

  <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
</body>
</html>
