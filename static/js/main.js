$(document).ready(function() {

    $("header input[name='new-series']").keydown(function(e) {
        if(e.which == 13) {
            // Enter key was pressed
            SearchSeries.search({
                name: $(this).val()
            });
        }
    });

});
