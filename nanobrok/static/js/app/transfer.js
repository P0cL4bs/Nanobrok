$(document).ready(function() {
    $(document).on('click', '#btnCheckConnection', function() {
        console.log("init btnCheckConnection");
        $.ajax({
            url: '/api/v1/web/transfer/ping',
            type: 'GET',
            contentType: "application/json",
            dataType: "json",
            beforeSend: function(request) {
                $('#btnCheckConnection').addClass("disabled");
                addloadingButton(true, "btnCheckConnection", "Checking...");
            },
            complete: function() {
                console.log("btnCheckConnection: complete");
                addloadingButton(false, "btnCheckConnection", "Check connection");
            },
            success: function(data) {
                console.log("btnCheckConnection: success");
                $('#btnCheckConnection').removeClass("disabled");
                halfmoon.initStickyAlert({
                    content: data.message,
                    title: "Device online",
                    alertType: "alert-success",
                    fillType: "filled-lm"
                });
            },
            error: function(request, status, error) {
                console.log("btnCheckConnection Error:" + error);
                var myArr = JSON.parse(request.responseText);
                halfmoon.initStickyAlert({
                    content: myArr["message"],
                    title: "Device offline",
                    alertType: "alert-danger",
                    fillType: "filled-lm"
                });
                $('#btnCheckConnection').removeClass("disabled");
            }
        });

    });

    var dropzone = new Dropzone('#demo-upload', {
        previewTemplate: document.querySelector('#preview-template').innerHTML,
        parallelUploads: 2,
        timeout: 60000 * 2,
        thumbnailHeight: 120,
        thumbnailWidth: 120,
        headers: { "X-CSRFToken": csrf_token },
        maxFilesize: 15,
        filesizeBase: 1000,
        thumbnail: function(file, dataUrl) {
            if (file.previewElement) {
                file.previewElement.classList.remove("dz-file-preview");
                var images = file.previewElement.querySelectorAll("[data-dz-thumbnail]");
                for (var i = 0; i < images.length; i++) {
                    var thumbnailElement = images[i];
                    thumbnailElement.alt = file.name;
                    thumbnailElement.src = dataUrl;
                }
                setTimeout(function() { file.previewElement.classList.add("dz-image-preview"); }, 1);
            }
        }
    });

    dropzone.on("totaluploadprogress", function(progress) {
        document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
    });

    dropzone.on("queuecomplete", function(progress) {
        $('.progress-bar').addClass('bg-success');
        $('.cancel').hide();
    });

    document.querySelector("#actions .cancel").onclick = function() {
        dropzone.removeAllFiles(true);
    };
});