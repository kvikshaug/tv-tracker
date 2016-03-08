$(document).ready(function() {
    var footer = $("footer");

    footer.find("a.sync").click(function(e) {
        if(!confirm("Are you sure!?")) {
            e.preventDefault();
        }
    });

    $("h4.season").click(function() {
        $("table.episodes[data-season='" + $(this).attr('data-season') + "']").toggle();
    });

});
