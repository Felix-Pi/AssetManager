function load_recommendations(id, symbol) {
    $.ajax({
        url: "/api/asset/" + symbol + "/recommendations",
        success: function (dataset) {
            draw_stacked_recommendation_bar_chart(id, 'Recommendations', dataset, label_suffix = '')
        },
        error: function (error) {
           $(id + ' .card-body').html(error['responseJSON'])
        }
    });
}

function setup_stock() {
    // //console.log('LOADED: stock.js')
    load_historical_data('#linechart', symbol, $('#linechart .settings button.active'));
    load_recommendations('#recommendations', symbol);
}


$(document).ready(function () {
    setup_stock();

    /*
    Line Chart
     */

    $(document).on('click', '#linechart .settings button', function () {
        let elem = $(this)

        $.ajax({
            url: "/api/asset/" + $('#linechart').attr('data-symbol') + "/historical_data",
            data: {
                'days': elem.attr('data-days'),
                'period': elem.attr('data-period')
            },
            success: function (dataset) {
                dataset = JSON.parse(dataset)
                update_chart(linechart, dataset[0].median, dataset[0].timestamps)
            }
        });


        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');
    });

    $(document).on('click', '.asset_elem', function () {
        let elem = $(this)
        let id = '#linechart'
        let settings = $(id + ' .settings button.active')

        let title = elem.attr('data-title')
        let symbol = elem.attr('data-symbol')
        let price = elem.attr('data-price')

        $.ajax({
            url: "/api/asset/" + symbol + "/historical_data",
            data: {'days': settings.attr('data-days'), 'period': settings.attr('data-period')},
            success: function (dataset) {
                dataset = JSON.parse(dataset)
                update_chart(linechart, dataset[0].median, dataset[0].timestamps)
            }
        });


        set_active('.asset_elem', elem);

        //set card title
        $(id + ' .card-header span').text(title + ': ' + price);
    });

    $(document).on('click', '.asset_elem_subheader_absolute', function () {
        $('.asset_elem_subheader_absolute').hide();
        $('.asset_elem_subheader_relative').show();

    });
    $(document).on('click', '.asset_elem_subheader_relative', function () {
        $('.asset_elem_subheader_relative').hide();
        $('.asset_elem_subheader_absolute').show();

    });


});