$(document).ready(function() {

    /* Include CSRF-token when applicable in AJAX requests */
    if($("input[name='csrfmiddlewaretoken']").length > 0) {
        $.ajaxSetup({
            type: 'POST',
            cache: false
        });
        $(document).on('ajaxSend', function(event, xhr) {
            xhr.setRequestHeader("X-CSRFToken", $("input[name='csrfmiddlewaretoken']").val());
        });
    }

});
