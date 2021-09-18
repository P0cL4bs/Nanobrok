$(document).ready(function() {
    $('#divAreaToken').hide();

    $('input:checkbox').change(
        function() {
            if ($(this).is(':checked')) {
                $('#qrcodeToken').hide();
                $('#divAreaToken').show();
            } else {
                $('#qrcodeToken').show();
                $('#divAreaToken').hide();
            }
        });
});