function setup() {

    /* setup line chart */
    target = $('.asset_elem:first-child')
    elem = $('#linechart .settings button.active')

    title = target.attr('data-title');
    symbol = target.attr('data-symbol');
    price = target.attr('data-price');

    $.ajax({
        url: "/api/stock/historical_data/",
        data: {
            'symbols': target.attr('data-symbol'),
            'days': elem.attr('data-days'),
            'period': elem.attr('data-period')
        },
        success: function (result) {
            result = JSON.parse(result)
            result.colored = false;

            var id = '#linechart'
            $(id).attr('data-symbol', symbol)

            linechart = chart_linechart(id, 'Line chart', result, '€')
            $(id + ' .card-header').text(title + ' - ' + symbol + ': ' + price);
        }
    });


    /* setup stock distribution */
    $.ajax({
        url: "/api/portfolio/get_stock_distribution/",
        data: {'portfolio_id': portfolio_id},
        success: function (result) {
            result = JSON.parse(result)
            result.colored = true;

            var id = '#stock_distribution'
            stock_distribution_chart = chart_doughnut(id, 'Stock distrubution', result, '€', 'auto', "300")
            //stock_distribution_chart = draw_bar_chart(id, 'Stock distrubution', result, '€', 'auto', "300")

        }
    });

    // function update_chart_type(id, type1, type2) {
    //     var chart = $(id).getContext('2d');
    //     var data = {data: chart.data.datasets[0].data, labels: chart.data.labels = labels}
    //
    //     chart.destroy()
    // }

    /* setup sector distribution */
    $.ajax({
        url: "/api/portfolio/get_sector_distribution/",
        data: {'portfolio_id': portfolio_id},
        success: function (result) {
            result = JSON.parse(result)
            result.colored = true;

            var id = '#sector_distribution'

            var sector_distribution_chart = draw_bar_chart('#sector_distribution', 'Sector distribution', result, '%', 'auto', "300")
        }
    });

    /* setup country data */
    $.ajax({
        url: "/api/portfolio/get_country_data/",
        data: {'portfolio_id': portfolio_id},
        success: function (result) {
            result = JSON.parse(result)
            result.colored = true;

            let id = '#country_distribution'
            country_distribution_chart = draw_bar_chart(id, 'Country distribution', result, '', 'auto', '300')

        }
    });
}


$(document).ready(function () {
    setup();
    /* update stock */
    $(document).on('click', '.edit_stock_button', function () {
        let portfolio_id = $(this).attr("portfolio_id");
        let asset_id = $(this).attr("asset_id");

        $.ajax({
            method: "POST",
            url: "/api/select_single_asset_from_portfolio/",
            data: {portfolio_id: portfolio_id, asset_id: asset_id},
            success: function (data) {
                console.log(data)
                data = data[0]

                let modal_id = '#edit_stock_modal'

                $(modal_id + "_label").text(data['title'] + ' - ' + data['symbol'])
                $(modal_id + " .dbcol[col='id']").val(asset_id)

                setFormValuesFromDatabase(modal_id, data)

                $(modal_id).modal('show');
            }
        });

    });

    $(document).on('click', '#edit_stock_modal .submit_form', function () {
        data = serializeFormForDatabase('#edit_stock_modal')

        $.ajax({
            method: "POST",
            url: "/api/portfolio/update_stock/",
            data: data,
            success: function (data) {
                console.log('success: ', data)
                $('#edit_stock_modal').modal('hide');
            }
        });

    });


    /* add asset */
    $(document).on('click', '#add_stock_button', function () {
        $('#add_stock_modal').modal('show');
    });


    $(document).on('click', '#add_stock_modal .submit_form', function () {
        let portfolio_id = $(this).attr("portfolio_id");

        data = serializeFormForDatabase('#add_stock_modal')

        $.ajax({
            method: "POST",
            url: "/api/portfolio/add_stock/",
            data: data,
            success: function (data) {
                $('#add_stock_modal').modal('hide');
            }
        });

    });


    $(document).on('click', '#doughnut_sector', function (e, f) {

        var activePoints = sector_chart.getElementAtEvent(e);

        if (activePoints[0] === undefined) {
            // $("#sector_distribution .sector").removeClass('hidden');
            // $("#sector_distribution .sector_assets").addClass('hidden');
        } else {
            let index = activePoints[0]._index;

            let sector = activePoints[0]._chart.data.labels[index]

            $("#sector_distribution .sector").addClass('hidden')
            $("#sector_distribution .sector_" + sector).removeClass('hidden')

            $("#sector_distribution .sector_assets").addClass('hidden')
            $("#sector_distribution .sector_assets_" + sector).removeClass('hidden')

            $(this).find('.card-footer').slideDown();
        }
    });

    $(document).on('click', '#sector_distribution .sector_title', function (e, f) {
        e.preventDefault();
        let sector = $(this).text()

        $("#sector_distribution .sector").addClass('hidden')
        $("#sector_distribution .sector_" + sector).removeClass('hidden')

        $("#sector_distribution .sector_assets").addClass('hidden')
        $("#sector_distribution .sector_assets_" + sector).removeClass('hidden')

    });


    /*
    Line Chart
     */

    $(document).on('click', '#linechart .settings button', function () {
        let elem = $(this)

        $.ajax({
            url: "/api/stock/historical_data/",
            data: {
                'symbols': $('#linechart').attr('data-symbol'),
                'days': elem.attr('data-days'),
                'period': elem.attr('data-period')
            },
            success: function (dataset) {
                dataset = JSON.parse(dataset)

                linechart.data.datasets[0].data = dataset[0].median;
                linechart.data.labels = dataset[0].timestamps;
                linechart.update();
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
            url: "/api/stock/historical_data/",
            data: {'symbols': symbol, 'days': settings.attr('data-days'), 'period': settings.attr('data-period')},
            success: function (dataset) {
                dataset = JSON.parse(dataset)

                linechart.data.datasets[0].data = dataset[0].median;
                linechart.data.labels = dataset[0].timestamps;
                linechart.update();
            }
        });


        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

        //set card title
        console.log(elem.find('.asset_title').attr('text'))
        $(id + ' .card-header').text(title + ' - ' + symbol + ': ' + price);
    });


});