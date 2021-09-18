function addloadingButton(status, button_id, label_button) {
    if (status) {
        $('#' + button_id).html(' <i id="loading_button" class="fa fa-spinner fa-spin"/> ' + label_button);
    } else {
        $('#loading_button').remove();
        $('#' + button_id).html(label_button);
    }
}

$(document).ready(function() {

    setTimeout(function loop() {
        $.ajax({
            url: '/update/sidebarHeader',
            type: 'GET',
            contentType: "application/json",
            beforeSend: function(request) {
                console.log("init: sidebar update");
            },
            complete: function() {
                console.log("sidebar: complete");
            },
            success: function(data) {
                console.log("success: " + data)
                $('#header_sidebar').html(data);
            },
            error: function(request, status, error) {
                console.log("sidebar Error:" + error);
            }
        });

        setTimeout(loop, 10000);
    }, 10000);

});