let map;
let markers = [];
let NUMBER = 0;

let bus_line_array = ["1", "3", "5", "11", "48", "101", "102", "104", "105", "106", "107", "108", "113", "114", "115", "116", "117", 
"119", "121", "312", "604", "655", "704", "705", "706", "911", "912", "1002", "1*",]

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
   

    openModal();

    // 클릭 이벤트 리스너 추가
    marker.addListener('click', function () {
        selectedMarker = marker;
        openModal();
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
    NUMBER = markers.length

    marker.addListener('click', function(){
        selectedMarker = marker;
        openModal();
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

//버스 노선 체크 박스 상태에 따라 보이고 안 보이도록 하기
function displayInput() {
    //체크 박스 찾기
    const checkbox = document.getElementById('bus_check');

    //checked 값에 따라 display 다르게 하기
    if (checkbox.checked) {
        document.getElementsById('bus_line').style.visibility ='visible';
    } else {
        document.getElementsById('bus_line').style.visibility ='hidden';

    }
}

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

    //입력창에 입력된 값 가져오기
    let lines = document.getElementById('bus_line').value;
    let lines_str = String(lines);
    //입력 값으로부터 버스 번호 배열 만들기
    let linesList = lines_str.split(",");
    const linesLength = linesList.length;
    const arrayLength = bus_line_array.length;
    //버스 번호 배열로부터 mobility index 소수점 뒷자리 만들기
    let decimal = "0";
    //저장할 String 만들기
    for (k = 0; k < arrayLength - 1; k++) {
        decimal = decimal.concat("0")
    }
    for (i = 0; i < linesLength; i++) {
        line_num = linesList[i];
        for (j = 0; j < arrayLength; j++) {
            array_num = bus_line_array[j];
            if (line_num == array_num) {
                decimal = replaceAt(j, "1", decimal);
            }
        }
    }
    //최종 모빌리티 인덱스
    const dot = ".";
    decimal = dot.concat(decimal);
    mobilityIndex = String(mobilityIndex);
    mobilityIndex = mobilityIndex.concat(decimal);
    
    updateMarker(NUMBER-1, mobilityIndex)
    //닫기
    closeModal();
});


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

//마커 업로드
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

//마커 저장
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

//문자열의 특정 인덱스에 있는 characteristic 변경 함수
function replaceAt(index, replacement, input) {
    const str_length = input.length;
    if (index > str_length - 1) {
        return input
    } else {
        let former = input.substring(0, index);
        let latter = input.substr(index + 1, str_length - former.length - 1);
        let result = former.concat(replacement);
        result = result.concat(latter);

        return result;
    }
}