let map;
let markers = [];
let NUMBER = 0;

function initMap() {
    // 지도 초기화 및 중앙 위치 설정
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 36.3722, lng: 127.3604 },
        zoom: 16
    });


    // 클릭 이벤트 리스너 추가
    map.addListener('click', function (event) {
        addMarker(event.latLng, NUMBER, 0);
        NUMBER++;
    });

}

function addMarker(location, number, cValue) {
    // 마커 생성
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        label: number.toString(), // 마커 레이블로 번호 표시
        customValue: cValue
    });

    // 마커를 markers 배열에 추가
    markers.push({ number, marker });

    openModal(number);

    // 클릭 이벤트 리스너 추가
    marker.addListener('click', function () {
        selectedMarker = marker;
        openModal(number);
    });

    
}

function addPreviousMarker(location, number, cValue){
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        label: number.toString(),
        customValue: cValue
    })

    markers.push({ number, marker })

    marker.addListener('click', function(){
        selectedMarker = marker;
        openModal(number);
    });
    
}


function removeMarker(markerToRemove) {
    // markers 배열에서 해당 마커 제거
    markers = markers.filter(item => item.marker !== markerToRemove);

    // 마커 지도에서 제거
    markerToRemove.setMap(null);
    NUMBER--;
}

function updateMarker(index, cValue) {
    if (index >= 0 && index < markers.length) {
        const markerInfo = markers[index];
        markerInfo.customValue = cValue;
        console.log(markers)
    } else {
        alert('Invalid marker index');  
    }
}

function openModal(index) {
    const modal = document.getElementById('modal');
    modal.style.display = 'block';
    
    //Okay 버튼 클릭 시
    document.getElementById('okay').addEventListener('click', function () {
        //체크박스에서 체크된 것 가져오기
        const query = 'input[name="Mobility"]:checked';
        const selectedEls = 
            document.querySelectorAll(query);

        //value 가져오기: 체크된 값 모두 더하기
        let mobilityIndex = 0;
        selectedEls.forEach((el) => {
            mobilityIndex += Number(el.value);
        });

        //마커 인덱스
        index = markers[index-1].marker.label
        updateMarker(index-1, mobilityIndex)
        //닫기
        closeModal();
    });
}

function closeModal() {
    const modal = document.getElementById('modal');
    modal.style.display = 'none';
}



function loadMarkersFromJSON(jsonData) {
    // 이전에 추가한 마커 삭제
    markers.forEach(item => item.marker.setMap(null));
    markers = [];
    index = 1;
    // JSON 데이터 파싱
    const markerData = JSON.parse(jsonData);

    // 마커 추가
    markerData.forEach(data => {
        const location = { lat: data.lat, lng: data.lng };
        addPreviousMarker(location, data.number, data.customValue);
        index++;
    });

    NUMBER = index;
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
        number: item.number,
        customValue: item.customValue
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



// 모달 다이얼로그에서 제거 버튼 클릭 시
document.getElementById('removeMarkerButton').addEventListener('click', function () {
    if (selectedMarker) {
        removeMarker(selectedMarker);
        selectedMarker = null;
    }
    closeModal();
});