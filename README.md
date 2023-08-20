<!DOCTYPE html>
<html>
<head>
  <title>경로 탐색 예제</title>
  <link rel="stylesheet" href="styles.css">
  <script src="path-to-your-js-file.js"></script>
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
</body>
</html>
