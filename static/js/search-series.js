(function(SearchSeries, $, undefined) {

    $(document).ready(function() {
        $("header input[name='new-series']").typeahead({
            source: SearchSeries.search,
            minLength: 3
        });
    });

    SearchSeries.search = function(query, process) {
        $.ajax({
            url: '/søk/',
            data: 'query=' + encodeURIComponent(query)
        }).done(function(result) {
            process(JSON.parse(result))
        }).fail(function(result) {
            alert("AJAX query failed, 500 from server? Response:\n\n" + result.responseText)
            process([]);
        });
    }

}(window.SearchSeries = window.SearchSeries || {}, jQuery ));
