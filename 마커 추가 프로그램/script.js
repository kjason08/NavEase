let map;
let markers = [];
let NUMBER = 1;

function initMap() {
    // 지도 초기화 및 중앙 위치 설정
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 36.3722, lng: 127.3604 },
        zoom: 16
    });


    // 클릭 이벤트 리스너 추가
    map.addListener('click', function (event) {
        addMarker(event.latLng, NUMBER);
        NUMBER++;
    });

}

function addMarker(location, number) {
    console.log("되는중");
    // 마커 생성
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        label: number.toString() // 마커 레이블로 번호 표시
    });

    // 클릭 이벤트 리스너 추가
    marker.addListener('click', function () {
        removeMarker(marker);
    });

    // 마커를 markers 배열에 추가
    markers.push({ number, marker });
}

function removeMarker(markerToRemove) {
    // markers 배열에서 해당 마커 제거
    markers = markers.filter(item => item.marker !== markerToRemove);

    // 마커 지도에서 제거
    markerToRemove.setMap(null);
    NUMBER--;
}

function loadMarkersFromJSON(jsonData) {
    // 이전에 추가한 마커 삭제
    markers.forEach(item => item.marker.setMap(null));
    markers = [];

    // JSON 데이터 파싱
    const markerData = JSON.parse(jsonData);

    // 마커 추가
    markerData.forEach(data => {
        const location = { lat: data.lat, lng: data.lng };
        addMarker(location, data.number);
    });
}

document.getElementById('loadButton').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            const jsonData = e.target.result;
            loadMarkersFromJSON(jsonData);
        };

        reader.readAsText(file);
    }
});

document.getElementById('saveButton').addEventListener('click', function () {
    const markerData = markers.map(item => ({
        lat: item.marker.getPosition().lat(),
        lng: item.marker.getPosition().lng(),
        number: item.number
    }));

    const jsonData = JSON.stringify(markerData);

    // JSON 파일 다운로드
    const blob = new Blob([jsonData], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'markers.json';
    a.click();
});
