$(document).ready(function() {
    $('#select_netscan_networks').change(function() {
        console.log("current date: " + $(this).val());
        var networkScanDate = { date: $(this).val() }
        $.ajax({
            url: '/netscan/action/viewScanDevices',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(networkScanDate),
            beforeSend: function(request) {

                //addloadingButton(true, "btnCheckConnection", "Checking...");
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            complete: function() {
                console.log("select_netscan_networks: complete");
                //addloadingButton(false, "btnCheckConnection", "Check connection");
            },
            success: function(data) {
                console.log("select_netscan_networks: success");
                $('#content_network_scanner').html(data);
                halfmoon.initStickyAlert({
                    content: "The data load is successfully",
                    title: "Network Scanner View",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("select_netscan_networks Error:" + error);
                var myArr = JSON.parse(request.responseText);
                halfmoon.initStickyAlert({
                    content: myArr["message"],
                    title: "Error: Bad request",
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
            }
        });
    });

    $(document).on('click', '#btnFindDevices', function() {
        console.log("init btnFindDevices");
        $.ajax({
            url: '/netscan/action/startScanDevices',
            type: 'GET',
            timeout: 2000 * 60,
            contentType: "application/json",
            beforeSend: function(request) {
                $('#btnFindDevices').addClass("disabled");
                $("#select_netscan_networks").val('0');
                addloadingButton(true, "btnFindDevices", "Scanning...");
            },
            complete: function() {
                console.log("btnFindDevices: complete");
                addloadingButton(false, "btnFindDevices", "Find devices");
            },
            success: function(data) {
                console.log("btnFindDevices: success");
                $('#btnFindDevices').removeClass("disabled");
                $('#content_network_scanner').html(data);
                halfmoon.initStickyAlert({
                    content: "The device has been successfully",
                    title: "Network Scanner Finder",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("btnFindDevices Error:" + error);
                halfmoon.initStickyAlert({
                    content: "Error: " + error,
                    title: "Error: Timeout request",
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
                $('#btnFindDevices').removeClass("disabled");
            }
        });

    });
});