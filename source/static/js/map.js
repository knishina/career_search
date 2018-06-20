d3.json("/data", function(error, response) {
    if (error) throw error;

    var sum_latitudes = 0;
    var sum_longitudes = 0;
    for (var i=0; i<response.length; i++) {
        sum_latitudes += response[i].latitude;
        sum_longitudes += response[i].longitude;
    }
    var average_latitude = sum_latitudes/(response.length);
    var average_longitude = sum_longitudes/(response.length);
    var centered = [average_latitude, average_longitude];

    var myMap = L.map("map", {
        center: centered,
        zoom: 10
    });
    var access_token = "";
    L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=" + access_token).addTo(myMap);
    
    for (var i=0; i<response.length; i++) {
        L.marker([response[i].latitude, response[i].longitude]).bindPopup(`${response[i].company}<hr><a style="font-size:12px"target="_blank" href=${response[i].url}>${response[i].title}</a>`).addTo(myMap);
    };
});
