$(document).ready(function() {

    $(document).on('click', '.networkAction', function() {

        var member_id = $(this).attr('id');
        console.log(member_id);
        $('#actions_network_div').attr('current_ip', member_id);

        // var name = $('#nameInput' + member_id).val();
        // var email = $('#emailInput' + member_id).val();
        $('#div_wifiInfo').append('<div class="content-wrapper" id="loading"> \
        <div class="d-flex h-full align-items-center justify-content-center flex-column"> \
        <div class="spinner"></div></div></div>');


        setTimeout(function() {
            console.log("sending request ");
            req = $.ajax({
                url: '/network_actions/' + member_id,
                type: 'GET'
            });


            req.done(function(data) {
                $('#actions_network_div').html(data);
                $('#btn_view_action').removeClass("disabled")
                $('#select_network_actions').removeAttr("disabled")
                $('#dropdown_network_actions').removeAttr("disabled")
                $('#loading').remove()
            });
        }, 2000);
    });


    $(document).on('click', '#btn_view_action', function() {

        $('#div_wifiInfo').append('<div class="content-wrapper" id="loading"> \
        <div class="d-flex h-full align-items-center justify-content-center flex-column"> \
        <div class="spinner"></div></div></div>');

        var curent_date = $("#select_network_actions").val();
        var data_send = { date: curent_date }
        setTimeout(function() {
            req = $.ajax({
                url: '/network_views',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data_send),
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", csrf_token);
                },
            });


            req.done(function(data) {
                $('#loading').remove()
                $('#view_network_div').fadeOut(500).fadeIn(1000).delay(3000);
                $('#view_network_div').html(data);
            });
        }, 2000);
    });

    $(document).on('click', '#btn_action_delete_one', function() {

        $('#div_wifiInfo').append('<div class="content-wrapper" id="loading"> \
        <div class="d-flex h-full align-items-center justify-content-center flex-column"> \
        <div class="spinner"></div></div></div>');

        var curent_date = $("#select_network_actions").val();
        var data_send = { date: curent_date }
        setTimeout(function() {
            req = $.ajax({
                url: '/network_actions_delete',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data_send),
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", csrf_token);
                },
            });


            req.done(function(data) {
                $('#actions_network_div').html(data);
                $('#loading').remove()
                var alertContent = "The wifiInfo deleted successfully.";
                halfmoon.initStickyAlert({
                    content: alertContent,
                    title: "WifiInfo Alert"
                })
            });
        }, 2000);
    });
    $(document).on('click', '#btn_action_delete_all', function() {

        $('#div_wifiInfo').append('<div class="content-wrapper" id="loading"> \
        <div class="d-flex h-full align-items-center justify-content-center flex-column"> \
        <div class="spinner"></div></div></div>');

        var curent_date = $("#select_network_actions").val();
        var current_ip = $('#actions_network_div').attr('current_ip')
        var data_send = { ip: current_ip }
        setTimeout(function() {
            req = $.ajax({
                url: '/network_actions_delete_all',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data_send),
                beforeSend: function(request) {
                    request.setRequestHeader("X-CSRFToken", csrf_token);
                },
            });


            req.done(function(data) {
                $('#actions_network_div').html(data);
                $('#loading').remove()
                var alertContent = "The all wifiInfo selected has been deleted successfully.";
                halfmoon.initStickyAlert({
                    content: alertContent,
                    title: "WifiInfo Alert"
                })
            });
        }, 2000);
    });

});