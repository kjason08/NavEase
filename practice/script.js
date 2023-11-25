function initMap() {
    var kaist = {lat: 36.374, lng: 127.365};
    var map = new google.maps.Map(document.getElementById('map'), {
        center: kaist,
        zoom: 16
    });
}

document.getElementById('toggleButton').addEventListener('click', function() {
    var toggleSidebar = document.getElementById('toggleSidebar');
    if (toggleSidebar.style.left === '-250px' || toggleSidebar.style.left === '') {
        toggleSidebar.style.left = '50px'; // fixedSidebar 너비만큼 오른쪽으로 이동
    } else {
        toggleSidebar.style.left = '-250px'; // 원래 위치로 이동
    }
});

window.onload = initMap;
