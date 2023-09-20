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
    // 마커 생성
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        label: number.toString() // 마커 레이블로 번호 표시
    });

    // 클릭 이벤트 리스너 추가
    marker.addListener('click', function () {
        selectedMarker = marker;
        openModal();
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

function updateMarker(index, newNumber) {
    if (index >= 0 && index < markers.length) {
        const markerInfo = markers[index];
        markerInfo.number = newNumber;
        markerInfo.marker.setLabel(newNumber.toString());
    } else {
        alert('Invalid marker index');
    }
}

function openModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
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

// 마커 업데이트
document.getElementById('updateButton').addEventListener('click', function () {
    const currentMarkerIndex = parseInt(document.getElementById('currentMarkerIndex').value);
    const newMarkerIndex = parseInt(document.getElementById('newMarkerIndex').value);

    updateMarker(currentMarkerIndex - 1, newMarkerIndex); // 인덱스를 0부터 시작하므로 1을 빼줍니다.
    closeModal();
});

// 모달 다이얼로그에서 추가 버튼 클릭 시
document.getElementById('addMarkerButton').addEventListener('click', function () {
    if (selectedMarker) {
        const newIndex = markers.length;
        addMarker(selectedMarker.getPosition(), newIndex + 1);
    }
    closeModal();
});

// 모달 다이얼로그에서 제거 버튼 클릭 시
document.getElementById('removeMarkerButton').addEventListener('click', function () {
    if (selectedMarker) {
        removeMarker(selectedMarker);
        selectedMarker = null;
    }
    closeModal();
});