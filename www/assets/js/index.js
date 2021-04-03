$(document).ready(function () {


    /* setup stock distribution */
    $.ajax({
        url: "/api/index/get_asset_distribution/",
        success: function (result) {
            data = JSON.parse(result)
            var id = '#asset_distribution'

            asset_distribution_chart = chart_doughnut(id, 'Asset distribution', data, '€', 'auto', 150)

            asset_distribution_chart.options.circumference = Math.PI;
            asset_distribution_chart.options.rotation = -Math.PI;
            asset_distribution_chart.options.borderWidth = 0;
            asset_distribution_chart.options.cutoutPercentage = 65;
            asset_distribution_chart.update();
        }
    });

});