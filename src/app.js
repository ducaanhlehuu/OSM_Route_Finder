var SERVER_URL="http://127.0.0.1:8000"
var marker;
var map;
var start_marker;
var end_marker;
var startPoint = null;
var endPoint = null;
var selectedAlgorithm='astar';
var result_json;
var polyline;
let markers =[];
var line1;
var line2;
var executeTimeMs;
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    
    map = new Map(document.getElementById("map"), {
        center: { lat: 21.02645, lng: 105.83165 },
        zoom: 18,
    })
    marker = new google.maps.Marker({
        position: { lat: 21.02645, lng: 105.83165 }, 
        title: 'Phuong Quoc Tu Giam',
        map:map,
    });
    
    const detailWindow = new google.maps.InfoWindow({
        content: "<h3>Phường Quốc Tử Giám</h3><h5>21.0273° N, 105.8327° E</h5>"
    });

    marker.addListener("mouseover", () =>{
        detailWindow.open(marker.getMap(),marker);
    });
}
function setStartPoint() {
    google.maps.event.clearListeners(map, 'click');
    map.addListener('click', function (mapsMouseEvent) {
        delete_Markers_and_polyline();
        // Lưu tọa độ điểm bắt đầu
        if (polyline && polyline.getMap()) {
            // Xóa polyline khỏi bản đồ
            polyline.setMap(null);
        }
        startPoint = mapsMouseEvent.latLng;
        showAutoClosingAlert("Start point set: " + startPoint.toString(),3000);

        // Vẽ marker ngay khi click chuột
        var icon = 'http://maps.google.com/mapfiles/ms/micons/blue.png';
        if(start_marker) start_marker.setMap(null);
        start_marker = new google.maps.Marker({
            position: { lat: startPoint.lat(), lng: startPoint.lng() }, 
            title: 'Start point',
            map: map,
            icon: icon
        });
        const detailWindow = new google.maps.InfoWindow({
            content: "<div>Start point</div>"
        });
        start_marker.addListener("mouseover", () =>{
            detailWindow.open(map,start_marker);
        });
    });
}


function setEndPoint() {
    google.maps.event.clearListeners(map, 'click');
    map.addListener('click', function (mapsMouseEvent) {
        delete_Markers_and_polyline();
        if (polyline && polyline.getMap()) {
            // Xóa polyline khỏi bản đồ
            polyline.setMap(null);
        }
        endPoint = mapsMouseEvent.latLng;
        showAutoClosingAlert("End point set: " + endPoint.toString(),3000);

        if(end_marker) end_marker.setMap(null);
        var icon = 'http://maps.google.com/mapfiles/ms/micons/green.png';
        end_marker = new google.maps.Marker({
            position: { lat: endPoint.lat(), lng: endPoint.lng() }, 
            title: 'End point',
            map: map,
            icon: icon
        });
        const detailWindow = new google.maps.InfoWindow({
            content: "<div>End point</div>"
        });
        end_marker.addListener("mouseover", () =>{
            detailWindow.open(map,end_marker);
        });
    });
}

function startFindingWay() {
    if (startPoint && endPoint) {
        google.maps.event.clearListeners(map, 'click');
        delete_Markers_and_polyline();
        if (polyline && polyline.getMap()) {
            // Xóa polyline khỏi bản đồ
            polyline.setMap(null);
        }
        // Tạo đối tượng dữ liệu để chứa thông tin điểm xuất phát và đích
        const apiUrl = `${SERVER_URL}/${selectedAlgorithm}?pntdata=${startPoint.lat()},${startPoint.lng()},${endPoint.lat()},${endPoint.lng()}`;
        showAutoClosingAlert("Running.......",1000);
        // Gọi API sử dụng fetch
        fetch(apiUrl)
            .then(response => response.json())
            .then(result => {
                // Xử lý kết quả từ API ở đây
                console.log(result);
                result_json = result;
                
                const pathCoordinates = result_json["path"].map(x => ({ lat: x[0], lng: x[1] }));
                executeTimeMs = (result_json["computation_time"] * 1000).toFixed(2);
                showAutoClosingAlert("Execute time: " + executeTimeMs + "ms       \nPath length: " + result_json["cost"].toFixed(4) + " km         \n"+"Number of nodes in route: "+result_json["path"].length+"\nNumber of nodes traversed on the map: "+ result_json["numbers_of_moved_nodes"],2000);
                setTimeout(function() {
                    alert("Path found!");
                  }, 100);
                polyline = new google.maps.Polyline({
                    path: pathCoordinates,
                    geodesic: true,
                    strokeColor: "#FF0000",
                    strokeOpacity: 2.0,
                    strokeWeight: 2,
                });
                polyline.setMap(map);
                pathCoordinates.forEach((coordinate, index) => {
                    const marker = new google.maps.Marker({
                        position: coordinate,
                        map: map,
                        label: {
                            text: `${index + 1}`, // Nhãn để hiển thị số thứ tự
                            color: 'white', // Màu chữ
                            fontSize: '12px', // Kích thước chữ
                        },
                    });
                    // Thêm sự kiện khi di chuột qua để hiển thị thông tin chi tiết
                    const detailWindow = new google.maps.InfoWindow({
                        content: `<div>${coordinate.lat}° N, ${coordinate.lng}° E</div>`,
                    });

                    marker.addListener('mouseover', () => {
                        detailWindow.open(map, marker);
                    });
                    markers.push(marker);
                                    });
                line1 = new google.maps.Polyline({
                    path: [
                      { lat: startPoint.lat(), lng: startPoint.lng() },
                      { lat: pathCoordinates[0].lat, lng: pathCoordinates[0].lng },
                    ],
                    geodesic: true,
                    strokeColor: "#FF0000",
                    strokeOpacity: 2.0,
                    strokeWeight: 2,
                  });
                line2 = new google.maps.Polyline({
                    path: [
                      { lat: pathCoordinates[pathCoordinates.length-1].lat, lng: pathCoordinates[pathCoordinates.length-1].lng },
                      { lat: endPoint.lat(), lng: endPoint.lng() },
                    ],
                    geodesic: true,
                    strokeColor: "#FF0000",
                    strokeOpacity: 2.0,
                    strokeWeight: 2,
                  });
                line1.setMap(map);
                line2.setMap(map);
            })
            .catch(error => {
                console.error("Error calling API:", error);
                alert("Please select points around Quoc Tu Giam Ward");
            });
    } else {
        alert("Please set both start and end points before finding the way.");
    }
}

function setAlgorithm(algorithm) {
    selectedAlgorithm = algorithm;
    delete_Markers_and_polyline();
    if (polyline && polyline.getMap()) {
        // Xóa polyline khỏi bản đồ
        polyline.setMap(null);
    }
    // Remove 'active' class from all dropdown items
    const dropdownItems = document.querySelectorAll('.dropdown-item');
    dropdownItems.forEach(item => item.classList.remove('active'));

    // Add 'active' class to the selected item
    const selectedItem = document.querySelector(`.dropdown-item[href="#"][onclick="setAlgorithm('${algorithm}')"]`);
    if (selectedItem) {
        selectedItem.classList.add('active');
    }
    showAutoClosingAlert(`Selected algorithm: ${algorithm}`,3000);
}
function setMapOnAll(map) {
    for (let i = 0; i < markers.length; i++) {
      markers[i].setMap(map);
    }
}
  
  // Removes the markers from the map, but keeps them in the array.
function hideMarkers() {
    setMapOnAll(null);
}
  
  // Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
  }
  
  // Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    hideMarkers();
    markers = [];
  }
function delete_Markers_and_polyline(){
    if(markers.length>0) {
        hideMarkers();
        deleteMarkers();
        polyline.setMap(null);
        line1.setMap(null);
        line2.setMap(null);
    }
}
function showAutoClosingAlert(message, timeout) {
    var alertElement = document.getElementById('custom-alert');
    alertElement.innerText = message;
    alertElement.style.display = 'block';

    setTimeout(function() {
      alertElement.style.display = 'none';
    }, timeout);
  }
initMap()
