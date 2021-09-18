$(document).ready(function() {
    $(document).on('click', '#btn_update_apps', function() {

        $.ajax({
            url: '/apps/update',
            type: 'GET',
            beforeSend: function() {
                console.log("Downloading ");
                $('#btn_update_apps').addClass("disabled");
                addloadingButton(true, "btn_update_apps", "Sending...");
            },
            complete: function() {
                $('#btn_update_apps').removeClass("disabled");
                addloadingButton(false, "btn_update_apps", "Update All Apps");
            },
            success: function(data) {
                console.log("Request success data:" + data);
                $('#content_apps').fadeOut(1000).fadeIn(1000);
                $('#content_apps').html(data);
                console.log("Request finish with successfully")
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
});


function filter_apps() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("input_filter_apps");
    filter = input.value.toUpperCase();
    list_apps = document.getElementById("list_apps");
    for (i = 0; i < list_apps.childElementCount; i++) {
        txtValue = list_apps.children[i].id;
        console.log(txtValue);
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            list_apps.children[i].style.display = "";
            console.log(list_apps.children[i]);
        } else {
            list_apps.children[i].style.display = "none";
        }
    }
}


function clear_filter_apps() {
    var list_apps = document.getElementById("list_apps");
    var input = document.getElementById("input_filter_apps");
    input.value = "";
    for (i = 0; i < list_apps.childElementCount; i++) {
        list_apps.children[i].style.position = "";
        list_apps.children[i].style.left = "";
    }
}