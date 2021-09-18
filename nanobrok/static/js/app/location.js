var mymap;

function createMap() {
    mymap = L.map('mapid').setView([0, 0], 13);
    mymap.setZoom(1);

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
        maxZoom: 20,
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, ' +
            'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>' + ', <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(mymap);

    var popup = L.popup();

    function onMapClick(e) {
        popup
            .setLatLng(e.latlng)
            .setContent("Coordinates :" + e.latlng.toString())
            .openOn(mymap);
    }

    mymap.on('click', onMapClick);
}


function setMapLocation(address, latitude, longitude) {
    mymap.setZoom(17);
    var makers = L.marker([latitude, longitude]).addTo(mymap)
        .bindPopup(address + `<br> Coordinates: (${latitude}, ${longitude})`).openPopup();
    makers.on('click', function(e) {
        console.log(e.latlng);
    });
    mymap.panTo(new L.LatLng(latitude, longitude));
}

$(document).ready(function() {
    // init map
    createMap();


    // actions functions
    $(document).on('click', '#btnGetLocalizaiton', function() {

        $.ajax({
            url: '/api/v1/web/getCurrentLocation',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            beforeSend: function(request) {
                console.log("Downloading ");
                $('#btnGetLocalizaiton').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnGetLocalizaiton", "Sending request...");
            },
            complete: function() {
                $('#btnGetLocalizaiton').removeClass("disabled");
                addloadingButton(false, "btnGetLocalizaiton", "Locate My Device");
            },
            success: function(data) {
                console.log("Response:");
                console.log("status code:" + data.code);
                console.log("-> message :" + data.message);
                console.log("-> address:" + data.data["address"]);
                console.log("-> latitude:" + data.data["latitude"]);
                console.log("-> longitude:" + data.data["longitude"]);
                if (data.data["latitude"] != null && data.data["longitude"] != null) {
                    setMapLocation(data.data["address"], data.data["latitude"], data.data["longitude"])
                    halfmoon.initStickyAlert({
                        content: "The device sent location information, the location set up map successfully.",
                        title: "Location found successfully",
                        alertType: "alert-success",
                        fillType: "filled-lm"
                    });
                    $("#location_current_date").text(data.data["date"]);
                    $("#location_current_address").text(data.data["address"]);
                    $("#location_current_gmaps").attr("href", "https://maps.google.com/maps?daddr=" + data.data["latitude"] + "," + data.data["longitude"]);
                } else {
                    halfmoon.initStickyAlert({
                        content: "The device sent location unknown information, maybe the device location is turned off.",
                        title: "Location unknown",
                        alertType: "alert-secondary",
                        fillType: "filled-lm"
                    });
                }
            },
            error: function(request, status, error) {
                console.log("Download Error:" + error);
                var myArr = JSON.parse(request.responseText);
                halfmoon.initStickyAlert({
                    content: myArr["message"],
                    title: "" + error,
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
            }
        });
    });

    // history locaiton 
    $(document).on('click', '#btnGetHistory', function() {
        $("#mapid").hide();
    });

    $(document).on('click', '#btnClose', function() {
        $("#mapid").show();
    });

    $(document).on('click', '#btnViewLocation', function() {
        $("#mapid").show();
        var selected_id = $('#selected_id').val();
        console.log(selected_id);
        setMapLocation($('#l_address_' + selected_id).val(),
            $('#l_latitude_' + selected_id).val(),
            $('#l_longitude_' + selected_id).val());

    });

    $('a.list_ul').click(function(e) {
        $('#selected_id').val($(this)[0].id);
    });

    // init set last location
    setMapLocation($('#location_address_id').val(),
        $('#location_latitude_id').val(),
        $('#location_longitude_id').val());
});