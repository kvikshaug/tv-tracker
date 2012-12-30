$(document).ready(function() {

    var ep_table = $("table.episodes");
    ep_table.find("tr.season").click(function() {
        ep_table.find("tr.episode[data-season='" + $(this).attr('data-season') + "']").toggle();
    });

});
