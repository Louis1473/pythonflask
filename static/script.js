let map;
let service;
let infowindow;

function initMap() {
    const takamatsu = new google.maps.LatLng(34.3428, 134.0466);

    map = new google.maps.Map(document.getElementById('map'), {
        center: takamatsu,
        zoom: 12
    });

    const marker = new google.maps.Marker({
        position: takamatsu,
        map: map
    });

    service = new google.maps.places.PlacesService(map);
    infowindow = new google.maps.InfoWindow();
}

function searchPlaces() {
    const query = document.getElementById('place-query').value;
    const request = {
        location: map.getCenter(),
        radius: '5000',
        query: query
    };

    service.textSearch(request, function(results, status) {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            results.forEach(place => {
                const marker = new google.maps.Marker({
                    map: map,
                    position: place.geometry.location
                });

                google.maps.event.addListener(marker, 'click', function() {
                    service.getDetails({ placeId: place.place_id }, function(details, status) {
                        if (status === google.maps.places.PlacesServiceStatus.OK) {
                            infowindow.setContent(`
                                <div>
                                    <h3>${details.name}</h3>
                                    <p>${details.formatted_address}</p>
                                    <p>評価: ${details.rating} (${details.user_ratings_total} 口コミ)</p>
                                    <p>${details.formatted_phone_number}</p>
                                    <p><a href="${details.url}" target="_blank">詳細を見る</a></p>
                                    <p><img src="${details.photos ? details.photos[0].getUrl() : ''}" alt="店の外観" style="width:100%;"></p>
                                </div>
                            `);
                            infowindow.open(map, marker);
                        }
                    });
                });
            });
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    initMap();
});
