$(document).ready(function() {
    var status_req = false;

    $(document).on('click', '#btnStartEventsRequest', function() {

        $('#btnStopEventsRequest').removeClass("disabled")

        $('#btnStartEventsRequest').addClass("disabled")
        status_req = true;
        getUpdateLogs();
        showAlertStartMonitorLogs();
    });

    $(document).on('click', '#btnStopEventsRequest', function() {
        if (status_req) {
            $('#btnStartEventsRequest').removeClass("disabled")
            $('#btnStopEventsRequest').addClass("disabled")
            status_req = false;
            stopAlertStartMonitorLogs();
        }
    });

    function getUpdateLogs() {
        setTimeout(function() {
            $.ajax({
                url: '/events/update',
                type: 'GET',
                beforeSend: function() {
                    console.log("Downloading ");
                },
                complete: function() {
                    if (status_req) {
                        getUpdateLogs();
                    }
                },
                success: function(data) {
                    console.log("Download Success ");
                    $('#content_table_events').html(data);
                }
            });
        }, 5000);
    }
});


function showAlertStartMonitorLogs() {
    halfmoon.initStickyAlert({
        content: "The real time monitor events has been started successfully",
        title: "Start to events monitor"
    });
}

function stopAlertStartMonitorLogs() {
    halfmoon.initStickyAlert({
        content: "The real time monitor events has been stopped",
        title: "Stop to events monitor"
    });
}

function filter_events() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("input_filter_table");
    filter = input.value.toUpperCase();
    table = document.getElementById("table_packet_data");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[1];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}


function filter_events_by_packet_type(packet_type) {
    var input, filter, table, tr, td, i, txtValue;
    filter = packet_type;
    table = document.getElementById("table_packet_data");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        console.log(td);
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}