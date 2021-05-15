function setup() {
    load_newsfeed(portfolio_symbols);

    /* setup line chart */
    target = $('.asset_elem:first-child')
    title = target.attr('data-title');
    symbol = target.attr('data-symbol');
    price = target.attr('data-price');

    /* setup stock distribution */
    $.ajax({
        url: '/api/portfolio/' + portfolio_id + '/stock_distribution',
        success: function (result) {
            result.colored = true;
            result.data = result.data_relative;

            var id = '#stock_distribution'
            stock_distribution_chart = chart_doughnut(id, 'Stock distrubution', result, '%', 'auto', 200)
            //stock_distribution_chart = draw_bar_chart(id, 'Stock distrubution', result, '€', 'auto', "300")

        }
    });

    /* setup sector distribution */
    $.ajax({
        url: '/api/portfolio/' + portfolio_id + '/sector_distribution',
        success: function (result) {
            result.colored = true;
            result.data = result.data_relative;

            var id = '#sector_distribution'

            var sector_distribution_chart = bar_chart('#sector_distribution', 'Sector distribution', result, '%', 'auto', 200)
        }
    });
    /* setup industry distribution */
    $.ajax({
        url: '/api/portfolio/' + portfolio_id + '/industry_distribution',
        success: function (result) {
            result.colored = true;
            result.data = result.data_relative;

            var id = '#industry_distribution'

            var sector_distribution_chart = bar_chart('#industry_distribution', 'Industry distribution', result, '%', 'auto', 200)
        }
    });

    /* setup country data */
    $.ajax({
        url: '/api/portfolio/' + portfolio_id + '/country_distribution',
        success: function (result) {
            result.colored = true;
            result.data = result.data_relative;

            let id = '#country_distribution'
            country_distribution_chart = bar_chart(id, 'Country distribution', result, '%', 'auto', 330)

        }
    });

    load_historical_data('#linechart', portfolio_id, $('#linechart .settings button.active'), action='init', 'portfolio')
}


$(document).ready(function () {
    setup();
    /* update stock */
    $(document).on('click', '.edit_stock_button', function () {
        let portfolio_id = $(this).attr("portfolio_id");
        let asset_id = $(this).attr("asset_id");

        $.ajax({
            method: "GET",
            url: '/api/portfolio/' + portfolio_id + '/asset' + asset_id,
            success: function (data) {
                //console.log(data)
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
                //console.log('success: ', data)
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

    /* add stock modal */
    /* input box for symbol: search yahoo finance */
    $(document).on('input', '#add_stock_modal .dbcol[col=symbol]', function () {
        let elem = $('#add_stock_modal .dbcol[col=symbol]');
        let results = elem.parent().find('.results');

        //console.log('val: ', elem.val());
        results.show()
        results.html('')

        $.ajax({
            method: "GET",
            url: '/api/stock/yahoo_search_de/',
            data: {'input': elem.val()},
            success: function (data) {
                //console.log('data', data);
                data = data['ResultSet']['Result'];
                //console.log(data);
                results.html('');

                for (let i = 0; i < data.length; i++) {
                    var item = data[i];
                    //console.log(item)
                    html = '' +
                        '<a class="result" href="" data-symbol="' + item['symbol'] + '" data-title="' + item['name'] + '">' +
                        '   <div class="content">' +
                        '       <div class="title">' + item['name'] + '</div>' +
                        '       <div class="description">' + item['symbol'] + ' - ' + item['exch'] + '</div>' +
                        '   </div>' +
                        '</a>';
                    results.append(html);
                }

            }
        });

    });

    $(document).on('click', '#add_stock_modal #search_symbol .results .result', function (e) {
        e.preventDefault();

        let elem = $(this);
        let target_symbol = $('#add_stock_modal .dbcol[col=symbol]');
        let target_title = $('#add_stock_modal .dbcol[col=title]');

        target_symbol.val(elem.attr('data-symbol'));
        target_title.val(elem.attr('data-title'));
        $('#add_stock_modal #search_symbol .results').html('').hide();

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

        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

        load_historical_data('#linechart', portfolio_id, $('#linechart .settings button.active'), action = 'update', 'portfolio')
    });

    $(document).on('click', '.asset_elem', function () {
        let elem = $(this);
        let id = '#linechart';
        let settings = $(id + ' .settings button.active');

        let title = elem.attr('data-title');
        let symbol = elem.attr('data-symbol');
        let price = elem.attr('data-price');

        $(id).attr('data-symbol', symbol);

        $.ajax({
            url: "/api/asset/" + symbol + "/historical_data",
            data: {
                'period': settings.attr('data-period'),
                'interval': settings.attr('data-interval'),
            },
            success: function (result) {
                result = JSON.parse(result)

                result.data = Object.values(result['Median'])
                result.labels = Object.values(result['timestamps'])
                result.colored = false;
                result.title = symbol;


                add_dataset_to_chart(linechart, result)
            }
        });


        set_active('.asset_elem', elem);

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