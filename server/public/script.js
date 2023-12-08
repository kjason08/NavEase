let map;
let marker;
let watchId = null;
let latLngs = [];
var currentPath = null; // 현재 그려진 라인을 저장하는 전역 변수

function initMap() {
  var kaist = {lat: 36.374, lng: 127.365};
  map = new google.maps.Map(document.getElementById('map'), {
      center: kaist,
      zoom: 18
  });

  loadMarkerData('/markers', function(markers) {
    // Creating LatLng objects from the marker data (markers not displayed on the map)
    markers.forEach(function(markerData) {
        var latLng = new google.maps.LatLng(markerData.lat, markerData.lng);
        latLngs[markerData.number] = latLng;
    });
    
});
}

document.getElementById('dataForm').addEventListener('submit', function(e) {
    e.preventDefault();
    

    // 체크박스 값에 따라 배열 생성
    let transportationOptions = [];
    if (document.getElementById('option1').checked) transportationOptions.push(10000); // 도보
    if (document.getElementById('option2').checked) transportationOptions.push(1000); // 타슈
    if (document.getElementById('option3').checked) transportationOptions.push(100); // 자전거
    if (document.getElementById('option4').checked) transportationOptions.push(10); // 지하철
    if (document.getElementById('option5').checked) transportationOptions.push(1); // 버스

    console.log("교통 수단 선택:", transportationOptions);

    // 슬라이더 값 출력
    let sliderValue = document.getElementById('filter-range').value;
    console.log("슬라이더 값:", sliderValue);
  
    var value1 = document.getElementById("startLocation").value;
    var value2 = document.getElementById("endLocation").value;
    var value3 = transportationOptions
    var value4 = (Math.floor(sliderValue/10)).toString()
    var value5 = (sliderValue%10).toString()

    fetch('/getPythonData', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ value1, value2, value3, value4, value5 }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data received:', data);
        connectMarkers(data[0]);
        connectMarkers1(data[1]);
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById("routeButton").addEventListener('click', function() {
  var additionalSidebar = document.getElementById('additionalSidebar');
  if (additionalSidebar.style.right === '-250px' || additionalSidebar.style.right === '') {
      additionalSidebar.style.right = '0px'; // 사이드바를 오른쪽에서 슬라이드
  } else {
      additionalSidebar.style.right = '-250px'; // 사이드바를 다시 숨김
  }
});


document.getElementById('closeSidebarButton').addEventListener('click', function() {
  var additionalSidebar = document.getElementById('additionalSidebar');
  additionalSidebar.style.right = '-250px'; // 사이드바를 닫음
});


function connectMarkers(dataArray) {
    console.log("Bus Route Number:", dataArray[3][0]);

    if (currentPath) {
        currentPath.setMap(null);
    }

    dataArray[1].forEach((index, i) => {
        if (i < dataArray[1].length - 1) {
        // 색상 결정
            var color;
            switch (dataArray[2][i]) {
                case 0:
                    color = '#000000'; // black
                    break;
                case 1:
                    color = '#FF0000'; // red
                    break;
                case 2:
                    color = '#0000FF'; // 파란색
                    break;
                case 3:
                    color = '#FFFF00'; // 노란색
                    break;
                case 4:
                    color = '#00FF00'; // green
                    break;
                default:
                    color = '#000000'; // 기본값은 black
            }

        // 세그먼트 경로 생성
        var pathSegment = new google.maps.Polyline({
            path: [latLngs[dataArray[1][i]], latLngs[dataArray[1][i + 1]]],
            geodesic: true,
            strokeColor: color,
            strokeOpacity: 1.0,
            strokeWeight: 2
        });

        // 세그먼트 경로를 지도에 추가
        pathSegment.setMap(map);
    }
    });      

          // dataArray[4] 값을 사이드바에 출력
      var dataDisplayElement = document.getElementById('dataDisplay');
      if (dataDisplayElement) {
        let minute = parseInt(60*dataArray[4])
        let str = minute.toString()
        dataDisplayElement.innerHTML = '시간: ' + str +'분';
      }


          // 세그먼트 컨테이너 요소 찾기
      var segmentContainer = document.getElementById('segmentContainer');
      if (segmentContainer) {
        // 컨테이너 초기화
        segmentContainer.innerHTML = '';
  
        // 세그먼트 생성
        for (var i = 0; i < dataArray[1].length - 1; i++) {
            var segment = document.createElement('div');
            segment.style.width = '20px';
            segment.style.height = '20px';
            segment.style.display = 'inline-block';
  
            // 색상 지정
            var color;
            switch (dataArray[2][i]) {
                case 0:
                    color = '#000000'; // black
                    break;
                case 1:
                    color = '#FF0000'; // red
                    break;
                case 2:
                    color = '#0000FF'; // 파란색
                    break;
                case 3:
                    color = '#FFFF00'; // 노란색
                    break;
                case 4:
                    color = '#00FF00'; // green
                    break;
                default:
                    color = '#000000'; // 기본값은 black
            }
            segment.style.backgroundColor = color;
  
            // 세그먼트 컨테이너에 추가
            segmentContainer.appendChild(segment);
          }
      }
};

function connectMarkers1(dataArray) {
    console.log("Bus Route Number:", dataArray[3][0]);

    if (currentPath) {
        currentPath.setMap(null);
    }

    dataArray[1].forEach((index, i) => {
        if (i < dataArray[1].length - 1) {
        // 색상 결정
            var color = '#FF00FF'; // purple;

        // 세그먼트 경로 생성
        var pathSegment = new google.maps.Polyline({
            path: [latLngs[dataArray[1][i]], latLngs[dataArray[1][i + 1]]],
            geodesic: true,
            strokeColor: color,
            strokeOpacity: 1.0,
            strokeWeight: 2
        });

        // 세그먼트 경로를 지도에 추가
        pathSegment.setMap(map);
    }
    });      
};

// loadMarkerData 함수 수정
function loadMarkerData(url, callback) {
  if (typeof callback !== 'function') {
      console.error('callback is not a function');
      return;
  }
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
      if (xhr.readyState == XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              callback(JSON.parse(xhr.responseText));
          } else {
              console.error('Failed to load marker data', xhr.status, xhr.statusText);
          }
      }
  };
  xhr.open('GET', url, true);
  xhr.send();
}


function toggleTracking() {
  if (watchId !== null) {
      // 위치 추적 중지
      navigator.geolocation.clearWatch(watchId);
      watchId = null;
      document.getElementById("toggleTracking").textContent = "위치 추적 시작";
  } else {
      // 위치 추적 시작
      if (navigator.geolocation) {
          watchId = navigator.geolocation.watchPosition(
              (position) => {
                  const pos = {
                      lat: position.coords.latitude,
                      lng: position.coords.longitude,
                  };

                  map.setCenter(pos);
                  if (marker) {
                      marker.setPosition(pos);
                  } else {
                      marker = new google.maps.Marker({
                          position: pos,
                          map: map,
                      });
                  }
              }, 
              (error) => {
                  console.error("Geolocation error: " + error.message);
              }, 
              { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
          );
          document.getElementById("toggleTracking").textContent = "위치 추적 중지";
      } else {
          console.error("Your browser doesn't support geolocation.");
      }
  }
}

document.getElementById("toggleTracking").addEventListener("click", toggleTracking);

function handleLocationError(browserHasGeolocation, pos) {
  console.log(browserHasGeolocation ?
              "Error: The Geolocation service failed." :
              "Error: Your browser doesn't support geolocation.");
  map.setCenter(pos);
}

document.getElementById('toggleButton').addEventListener('click', function() {
  var toggleSidebar = document.getElementById('toggleSidebar');
  if (toggleSidebar.style.left === '-250px' || toggleSidebar.style.left === '') {
      toggleSidebar.style.left = '50px'; // fixedSidebar 너비만큼 오른쪽으로 이동
  } else {
      toggleSidebar.style.left = '-250px'; // 원래 위치로 이동
  }
});

window.addEventListener('load', initMap);

function addMarkers() {
  var startLocation = document.getElementById('startLocation').value;
  var endLocation = document.getElementById('endLocation').value;

  var geocoder = new google.maps.Geocoder();

  geocoder.geocode({'address': startLocation}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
      map.setCenter(results[0].geometry.location);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });

  geocoder.geocode({'address': endLocation}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      new google.maps.Marker({
        map: map,
        position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}