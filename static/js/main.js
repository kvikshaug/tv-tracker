$(document).ready(function() {

    $("footer a.sync").click(function(e) {
        if(!confirm("Sikker!?")) {
            e.preventDefault();
        }
    });

    $("h4.season").click(function() {
        $("table.episodes[data-season='" + $(this).attr('data-season') + "']").toggle();
    });

});
