function progressbar(status, timeout) {
    if (status) {
        $('.progress-bar').show();
        $('.progress-bar').style = "width: 0%; transition=none;";
        $('.progress-bar').delay(1000).queue(function() {
            $(this).css({ "width": "100%", "transition": timeout + "s" });
        });
        return;
    }
    $('.progress-bar').css({ "width": "0%" });
    $('.progress-bar').hide();
    $('.progress-bar').clearQueue();
}

$(document).ready(function() {


    $(document).on('click', '#btnGetAudio', function() {
        var time_record = $("#inputTimeout").val();
        console.log("time record: " + time_record);
        if (!/^[0-9]+$/.test(time_record)) {
            halfmoon.initStickyAlert({
                title: "Timeout to record",
                content: "The timout field only allow numeric characters (in seconds).",
                alertType: "alert-secondary",
                fillType: "filled-lm"
            });
            return;
        }
        if (parseInt(time_record) > 50 && parseInt(time_record) > 0) {
            halfmoon.initStickyAlert({
                content: "The maximum value to record audio is 50 seconds.",
                title: "Maximum value to record audio",
                alertType: "alert-secondary",
                fillType: "filled-lm"
            });
            return;
        }
        $.ajax({
            url: '/commands/records/audio',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({ "time_record": parseInt(time_record) }),
            beforeSend: function(request) {
                console.log("starting: beforeSend");
                progressbar(true, time_record);
                request.setRequestHeader("X-CSRFToken", csrf_token);
                $('#btnGetAudio').addClass("disabled");
                addloadingButton(true, "btnGetAudio", "Send request...");
            },
            complete: function() {
                console.log("starting: complete");
                $('#btnGetAudio').removeClass("disabled");
                progressbar(false, time_record);
                addloadingButton(false, "btnGetAudio", "Send");
            },
            success: function(data) {
                console.log("starting: success");
                $('#list_audios').fadeOut(500).fadeIn(1000).delay(3000);
                $('#list_audios').html(data);
            },
            error: function(request, status, error) {
                console.log("starting: error");
                $('#btnGetAudio').removeClass("disabled");
                progressbar(false, time_record)
                addloadingButton(false, "btnGetAudio", "Send");
            }
        });

    });

    $(document).on('click', '#btnCheckPermission', function() {
        $.ajax({
            url: '/api/v1/web/commands/security/checkIsEnableAdmin',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: "",
            beforeSend: function(request) {
                console.log("checkIsEnableAdmin: beforeSend");
                $('#btnCheckPermission').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnCheckPermission", "Sending...");
            },
            complete: function() {
                console.log("checkIsEnableAdmin: complete");
                $('#btnCheckPermission').removeClass("disabled");
                addloadingButton(false, "btnCheckPermission", "Check permission");
            },
            success: function(data) {
                console.log("checkIsEnableAdmin: success");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Enabled admin successfully",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("checkIsEnableAdmin Error:" + error);
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

    $(document).on('click', '#btnSetLocked', function() {
        $.ajax({
            url: '/api/v1/web/commands/security/locknow',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: "",
            beforeSend: function(request) {
                console.log("locknow: beforeSend");
                $('#btnSetLocked').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnSetLocked", "Sending...");
            },
            complete: function() {
                console.log("locknow: complete");
                $('#btnSetLocked').removeClass("disabled");
                addloadingButton(false, "btnSetLocked", "Lock now");
            },
            success: function(data) {
                console.log("locknow: success");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Lock now successfully",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("locknow Error:" + error);
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

    $(document).on('click', '#btnSetMaxLock', function() {
        var time_inactive = $("#inputSetMaxLock").val();
        console.log("time max inactive to lock: " + time_inactive);
        if (!/^[0-9]+$/.test(time_inactive)) {
            halfmoon.initStickyAlert({
                title: "Maximum inactivity time lock",
                content: "The timout field only allow numeric characters (in seconds).",
                alertType: "alert-secondary",
                fillType: "filled-lm"
            });
            return;
        }
        if (parseInt(time_inactive) > 60 && parseInt(time_inactive) > 0) {
            halfmoon.initStickyAlert({
                content: "The maximum value to max inactivity is 60 seconds.",
                title: "Maximum value to max inactivity",
                alertType: "alert-secondary",
                fillType: "filled-lm"
            });
            return;
        }
        $.ajax({
            url: '/api/v1/web/commands/security/maxInactivityTimeLock',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({ "timeMs": time_inactive }),
            beforeSend: function(request) {
                console.log("maxInactivityTimeLock: beforeSend");
                $('#btnSetMaxLock').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnSetMaxLock", "Sending...");
            },
            complete: function() {
                console.log("maxInactivityTimeLock: complete");
                $('#btnSetMaxLock').removeClass("disabled");
                addloadingButton(false, "btnSetMaxLock", "Set");
            },
            success: function(data) {
                console.log("maxInactivityTimeLock: success");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Maximum inactivity time lock",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("maxInactivityTimeLock Error:" + error);
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

    $(document).on('click', '#btnMessageToast', function() {
        var message_toast = $("#inputMessageToast").val();
        var data_message = { message: message_toast }
        $.ajax({
            url: '/api/v1/web/commands/misc/messageToast',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(data_message),
            beforeSend: function(request) {
                console.log("messageToast: beforeSend");
                $('#btnMessageToast').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnMessageToast", "Sending...");
            },
            complete: function() {
                console.log("messageToast: complete");
                $('#btnMessageToast').removeClass("disabled");
                addloadingButton(false, "btnMessageToast", "Send");
            },
            success: function(data) {
                console.log("messageToast: success");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Message Toasts",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("maxInactivityTimeLock Error:" + error);
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

    $(document).on('click', '#btnSendClipboard', function() {
        var clipboard_option = $("#selectClipboardOption").val();
        var textareaData = $("#textareaDataText").val();
        if (clipboard_option == null) {
            halfmoon.initStickyAlert({
                content: "The select option can be not empty.",
                title: "Clipboard Option",
                alertType: "alert-danger",
                fillType: "filled-lm"
            });
            return
        }

        clipboard_data = { "action": clipboard_option, "content": textareaData }
        $.ajax({
            url: '/api/v1/web/commands/misc/clipboard',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(clipboard_data),
            beforeSend: function(request) {
                console.log("btnSendClipboard: beforeSend");
                $('#btnSendClipboard').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnSendClipboard", "Sending...");
            },
            complete: function() {
                console.log("btnSendClipboard: complete");
                $('#btnSendClipboard').removeClass("disabled");
                addloadingButton(false, "btnSendClipboard", "Apply");
            },
            success: function(resp) {
                console.log("btnSendClipboard: success");

                if (resp.data.content === 'null') {
                    halfmoon.initStickyAlert({
                        content: "Your app cannot access the Clipboard manager for background Apps on android 10 or higher.",
                        title: "Limited access to clipboard Data",
                        alertType: "alert-secondary",
                        fillType: "filled-dm"
                    });
                    return
                }
                halfmoon.initStickyAlert({
                    content: resp.message,
                    title: "Clipboard Successfully",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
                $("#textareaDataText").val(resp.data.content)
            },
            error: function(request, status, error) {
                console.log("maxInactivityTimeLock Error:" + error);
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

    $(document).on('click', '#btnPermissionCheck', function() {
        var permission = $("#inputPermission").val();
        if (!$("#inputPermission").val()) {
            halfmoon.initStickyAlert({
                content: "The permission field is empty",
                title: "Empty field",
                alertType: "alert-secondary",
                fillType: "filled-lm"
            });
            return;
        }
        $.ajax({
            url: '/commands/security/permission',
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify({ "permission": permission }),
            beforeSend: function(request) {
                $('#btnPermissionCheck').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnPermissionCheck", "Checking...");
            },
            complete: function() {
                console.log("btnPermissionCheck: complete");
                $('#btnPermissionCheck').removeClass("disabled");
                addloadingButton(false, "btnPermissionCheck", "Check");
            },
            success: function(data) {
                console.log("btnPermissionCheck: success");
                $('#resultPermission').fadeOut(0).html(data).fadeIn(1000);
            },
            error: function(request, status, error) {
                console.log("btnPermissionCheck: error");
                $('#btnPermissionCheck').removeClass("disabled");
                addloadingButton(false, "btnPermissionCheck", "Check");
            }
        });

    });

    $(document).on('click', '#btnStartAlarm', function() {

        var data_message = { status: true }
        $.ajax({
            url: '/api/v1/web/commands/security/alarm',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(data_message),
            beforeSend: function(request) {
                console.log("alarm: beforeSend");
                $('#btnStartAlarm').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnStartAlarm", "Sending...");
            },
            complete: function() {
                console.log("alarm: complete");
                addloadingButton(false, "btnStartAlarm", "Start");
            },
            success: function(data) {
                console.log("alarm: success");
                $('#btnStopAlarm').removeClass("disabled");
                $('#btnStartAlarm').addClass("disabled");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Message Toasts",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("alarm Error:" + error);
                var myArr = JSON.parse(request.responseText);
                halfmoon.initStickyAlert({
                    content: myArr["message"],
                    title: "" + error,
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
                $('#btnStartAlarm').removeClass("disabled");
            }
        });

    });

    $(document).on('click', '#btnStopAlarm', function() {

        var data_message = { status: false }
        $.ajax({
            url: '/api/v1/web/commands/security/alarm',
            type: 'POST',
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify(data_message),
            beforeSend: function(request) {
                console.log("alarm: beforeSend");
                $('#btnStopAlarm').addClass("disabled");
                request.setRequestHeader("X-CSRFToken", csrf_token);
                addloadingButton(true, "btnStopAlarm", "Sending...");
            },
            complete: function() {
                console.log("alarm: complete");
                addloadingButton(false, "btnStopAlarm", "Stop");
            },
            success: function(data) {
                console.log("alarm: success");
                $('#btnStartAlarm').removeClass("disabled");
                $('#btnStopAlarm').addClass("disabled");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Alarm ",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("alarm Error:" + error);
                var myArr = JSON.parse(request.responseText);
                halfmoon.initStickyAlert({
                    content: myArr["message"],
                    title: "" + error,
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
                $('#btnStartAlarm').removeClass("disabled");
            }
        });

    });

});