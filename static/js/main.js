$(document).ready(function() {
    var header = $("header");
    var footer = $("footer");

    var search_form = header.find("form.search");

    search_form.submit(function(e) {
        if(search_form.find("input[name='query']").val().length < 3) {
            alert("At least 3 characters for the search, please.");
            e.preventDefault();
        }
    });

    footer.find("a.sync").click(function(e) {
        if(!confirm("Are you sure!?")) {
            e.preventDefault();
        }
    });

    $("h4.season").click(function() {
        $("table.episodes[data-season='" + $(this).attr('data-season') + "']").toggle();
    });

});
