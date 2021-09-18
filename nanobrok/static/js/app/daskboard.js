$(document).ready(function() {
    $(document).on('click', '#btn_updateDashboard', function() {

        // $('#content_user_data').append('<div class="content-wrapper" id="loading"> \
        // <div class="d-flex h-full align-items-center justify-content-center flex-column"> \
        // <div class="spinner"></div></div></div>');


        // $('#btn_updateDashboard').addClass("disabled")

        $.ajax({
            url: '/updateDashboard',
            type: 'GET',
            beforeSend: function(request) {
                console.log("updating dashboard ");
                $('#btn_updateDashboard').addClass("disabled");
                addloadingButton(true, "btn_updateDashboard", "Loading...");
            },
            complete: function() {
                $('#btn_updateDashboard').removeClass("disabled");
                addloadingButton(false, "btn_updateDashboard", "Refresh");
            },
            success: function(data) {
                $('#content_user_data').fadeOut(1000).fadeIn(1000);
                $('#content_user_data').html(data);
            },
            error: function(request, status, error) {

            }
        });


        // setTimeout(function() {
        //     req = $.ajax({
        //         url: '/updateDashboard',
        //         type: 'GET'
        //     });


        //     req.done(function(data) {
        //         $('#content_user_data').fadeOut(1000).fadeIn(1000);
        //         $('#content_user_data').html(data);
        //     });
        // }, 2000);


    });
});