function setup() {
    load_newsfeed(symbol);

    /* setup stock and sector distribution */
    $.ajax({
            url: "/api/etf/get_top_holdings/",
            data: {'portfolio_id': portfolio_id, 'symbol': symbol},
            success: function (result) {
                let holdings = {'data': result.holdings.data, 'labels': result.holdings.labels, colored: true};
                let sectors = {
                    'data': result.sectorWeightings.data,
                    'labels': result.sectorWeightings.labels,
                    colored: true
                };

                let top_holdings_chart = chart_doughnut('#top_holdings', 'Top holdings', holdings, '%', 'auto', "300");
                let sector_distribution_chart = bar_chart('#top_sectors', 'Sector distribution', sectors, '%', 'auto', "300");
            }
        }
    );


    elem = $('#linechart .settings button.active')
    $.ajax({
        url: "/api/stock/historical_data/",
        data: {'symbols': symbol, 'days': elem.attr('data-days'), 'period': elem.attr('data-period')},
        success: function (data) {
            data = JSON.parse(data)
            linechart = chart_linechart('#linechart', 'Line chart', data, '€', '', '')

        }
    });

}


$(document).ready(function () {
    setup();

    /*
Line Chart
 */

    $(document).on('click', '#linechart .settings button', function () {
        let elem = $(this)

        $.ajax({
            url: "/api/stock/historical_data/",
            data: {
                'symbols': symbol,
                'days': elem.attr('data-days'),
                'period': elem.attr('data-period')
            },
            success: function (dataset) {
                dataset = JSON.parse(dataset)
                console.log(dataset)
                update_chart(linechart, dataset[0].median, dataset[0].timestamps)
            }
        });


        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');
    });


});