$(document).ready(function () {


    doughnut_asset_allocation_data = JSON.parse($('#doughnut_asset_allocation').attr('data-val').replaceAll('\'', '\"'))
    doughnut_asset_allocation_label = JSON.parse($('#doughnut_asset_allocation').attr('label-val').replaceAll('\'', '\"'))

    doughnut_asset_allocation = chart_doughnut('#doughnut_asset_allocation', 'Distrubution', doughnut_asset_allocation_data, doughnut_asset_allocation_label, '€', 'auto', 150)

    doughnut_asset_allocation.options.circumference = Math.PI;
    doughnut_asset_allocation.options.rotation = -Math.PI;
    doughnut_asset_allocation.options.borderWidth = 0;
    doughnut_asset_allocation.options.cutoutPercentage = 65;
    doughnut_asset_allocation.update();

});