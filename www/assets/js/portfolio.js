function setFormValuesFromDatabase(form_id, data) {
    console.log(data)
    //format: .dbcol needs attr: col="col_dame_in_data"
    $(form_id + ' .dbcol').each(function () {
        elem = $(this)
        col = elem.attr("col")

        elem.val(data[col])
    });

    $(form_id + ' .dbcol-opt').each(function () {
        elem = $(this)
        col = elem.attr("col")

        elem.val(data[col])
        $(form_id + '_' + col + '_' + data[col]).prop('selected', true);
    });

}


function serializeFormForDatabase(form_id) {

    result = {}

    $(form_id + ' .dbcol').each(function () {
        let elem = $(this);
        let val = elem.val();
        let key = elem.attr('col');

        result[key] = val;
    });

    $(form_id + ' .dbcol-opt').each(function () {
        let elem = $(this);
        let val = elem.children(':selected').attr('db-id');
        let key = elem.attr('col');

        result[key] = val;
    });

    return result;

}

$(document).ready(function () {

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


    symbols = []
    titles = []

    let max_symbols_for_chart = 1;
    let counter = 0;

    $('.asset_elem').each(function () {
        if (counter < max_symbols_for_chart) {
            symbols.push($(this).attr('data-symbol'));
            titles.push($(this).attr('data-title'));
            counter += 1;
        }

    })
    if (symbols.length > 1) {
        symbols = symbols.join(',');
        titles = titles.join(',');
    } else {
        symbols = symbols[0];
        titles = titles[0];
    }

    elem = $('#linechart_all_portfolios .settings button.active')
    $.ajax({
        method: "POST",
        url: "/api/stock/historical_data/",
        data: {'symbols': symbols, 'days': elem.attr('data-days'), 'period': elem.attr('data-period')},
        success: function (data) {
            let id = '#linechart_all_portfolios'
            linechart_all_portfolios = chart_linechart(id, 'Line chart', JSON.parse(data), '€')
            $(id + ' .card-header').text(titles + ' - ' + symbols);
        }
    });


    $.ajax({
        method: "GET",
        url: "/api/stock/country_data/",
        data: {'portfolio_id': portfolio_id},
        success: function (result) {
            result = JSON.parse(result)

            data = []
            labels = []


            console.log(result)
            for (let i = 0; i < result.length; i++) {
                data.push(result[i]['amount'])
                labels.push(result[i]['country'])
            }

            console.log(data, labels)

            let id = '#doughnut_country'
            doughnut_country = chart_doughnut(id, 'Country distribution', data, labels, '', 'auto', '150')

            doughnut_country.options.circumference = Math.PI;
            doughnut_country.options.rotation = -Math.PI;
            doughnut_country.update();


            $(id + ' .card-header').text(titles + ' - ' + symbols);


        }
    });

    $(document).on('click', '#linechart_all_portfolios .settings button', function () {
        let elem = $(this)

        $.ajax({
            method: "POST",
            url: "/api/stock/historical_data/",
            data: {'symbols': symbols, 'days': elem.attr('data-days'), 'period': elem.attr('data-period')},
            success: function (dataset) {
                dataset = JSON.parse(dataset)

                linechart_all_portfolios.data.datasets[0].data = dataset[0].median;
                linechart_all_portfolios.data.labels = dataset[0].timestamps;
                linechart_all_portfolios.update();
            }
        });


        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');
    });

    $(document).on('click', '.asset_elem', function () {
        let elem = $(this)
        let id = '#linechart_all_portfolios'
        let settings = $(id + ' .settings button.active')

        title = elem.attr('data-title')
        let symbol = elem.attr('data-symbol')

        $.ajax({
            method: "POST",
            url: "/api/stock/historical_data/",
            data: {'symbols': symbol, 'days': settings.attr('data-days'), 'period': settings.attr('data-period')},
            success: function (dataset) {
                dataset = JSON.parse(dataset)

                linechart_all_portfolios.data.datasets[0].data = dataset[0].median;
                linechart_all_portfolios.data.labels = dataset[0].timestamps;
                linechart_all_portfolios.update();
            }
        });


        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

        //set card title
        console.log(elem.find('.asset_title').attr('text'))
        $(id + ' .card-header').text(title + ' - ' + symbol);
    });


});