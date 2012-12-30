$(document).ready(function() {

    $("h4.season").click(function() {
        $("table.episodes[data-season='" + $(this).attr('data-season') + "']").toggle();
    });

});
