$(document).ready(function() {
    $(document).on('click', '#btn_updateExtensions', function() {

        $.ajax({
            url: '/extensions/action/getAllExtensions',
            type: 'GET',
            beforeSend: function(request) {
                addloadingButton(true, "btn_updateExtensions", "loading...");
            },
            complete: function() {
                console.log("extensions: complete");
                addloadingButton(false, "btn_updateExtensions", "Refresh");
            },
            success: function(data) {
                console.log("extensions: success");
                $('#content_extensions').html(data);
                halfmoon.initStickyAlert({
                    content: "The extensions has updated successfully",
                    title: "Extensions",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("extensions Error:" + error);
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
});