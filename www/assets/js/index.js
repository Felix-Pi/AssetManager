function setup() {
    load_newsfeed(all_symbols);
    /* setup stock distribution */
    $.ajax({
        url: "/api/index/get_asset_distribution/",
        success: function (result) {
            result = JSON.parse(result)
            var id = '#asset_distribution'

            result.data = result.data_relative;
            result.colored = true;

            asset_distribution_chart = chart_half_doughnut(id, 'Asset distribution', result, '%', 'auto', 150)


        }
    });
}

$(document).ready(function () {
    setup();


});