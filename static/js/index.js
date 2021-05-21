function setup() {
    load_newsfeed(all_symbols);
    /* setup stock distribution */
    $.ajax({
        url: "/api/index/" + user_id + "/asset_distribution",
        success: function (result) {
            var id = '#asset_distribution'

            result.data = result.data_relative;
            result.colored = true;

            asset_distribution_chart = chart_half_doughnut(id, 'Asset distribution', result, '%', 'auto', 125)


        }
    });

    $.ajax({
        url: "/api/index/" + user_id + "/monthly_transaction_data",
        success: function (result) {
            var id = '#monthly_transactions'
            let keys = result.keys

            result = result.data


            for (let i = 0; i < keys.length; i++) {
                var tr_type = result[keys[i]]
                var data = {}

                data.data = tr_type.data_absolute;
                data.labels = tr_type.labels;
                data.suffix = tr_type.suffix;
                data.colored = true;

                html = '<div class="ui label">' + tr_type['average'] + ' €' + ' <a class="detail">per month</a></div>' +
                    '<div class="ui label">' + tr_type['sum'] + ' €' + ' <a class="detail">total</a></div>' +
                    '<div class="ui label">' + tr_type['actions'] + ' actions <a class="detail">total</a></div>' +
                    '<div class="ui label">' + tr_type['actions_month'] + ' actions <a class="detail">per month</a></div>';

                data.title = 'Monthly Transactions: ' + tr_type.title + '~' + html;


                var chart_id = (id + '_' + keys[i]).replace('#', '')


                var btn_html = '<button class="ui button ' + (i === 0 ? 'active' : '') + '" data-attr="' + chart_id + '">' + tr_type.title + '</button>'
                $(id + ' .card-header .settings').append(btn_html)

                $(id + ' .card-body.main').append(
                    '<div id="' + chart_id + '">' +
                    '<div class="card-body tr_chart_container ' + (i === 0 ? 'active' : 'hidden') + '"></div>' +
                    '<div class="card-header hidden"><span></span></div>' +
                    '<div class="card-footer hidden"><span></span></div>' +
                    '</div>'
                );

                monthly_charts = {}

                monthly_charts[chart_id] = bar_chart('#' + chart_id, data.title, data, '', 'auto', 122)


            }

            $(id + ' .card-body.main .card-body').removeClass('card-body')
            $(id + ' .card-body.main .card-footer').removeClass('card-footer').addClass('footer')
            $(id + ' .card-body.main .card-header').removeClass('card-header').addClass('header')

            $(id + ' .card-footer span').html($(id + '_' + keys[0] + ' .footer span').html())

        }
    });

    //MAIN_NAVIGATION
    $(document).on('click', '#monthly_transactions .settings .button', function () {
        let elem = $(this);
        let target = elem.attr('data-attr');

        set_active('#monthly_transactions .settings', elem)

        $('#monthly_transactions .tr_chart_container').addClass('hidden');
        $('#monthly_transactions .card-footer span').html($('#' + target + ' .footer').html())

        var chart = get_instance_from_id(target + '_canvas')
        let data = chart.data.datasets[0].data.slice()
        chart.data.datasets[0].data = []

        $('#' + target + ' .tr_chart_container').removeClass('hidden');

        setTimeout(function () {
            chart.data.datasets[0].data = data
            chart.update()
        }, 30);


    });

}

function load_milestones(id, title) {
    $.ajax({
        url: "/api/index/" + user_id + "/milestones",
        success: function (result) {
            for (let i = 0; i < result.length; i++) {
                var milestone_title = result[i]['title']
                var milestone_id = 'milestone_' + result[i]['title']

                $(id + ' .card-body.main').append(
                    '<div id="' + milestone_id + '" class="tr_chart_container ' + (i === 0 ? 'active' : 'hidden') + '">' +
                    '<div class="card-body"></div></div>'
                );


                var dataset = {}

                dataset.median =Object.keys(result[i]['milestones'])
                console.log(result[i])
                // for (let j = 0; j < Object.keys(result[i]['milestones']).length; j++) {
                //     dataset.median.push(1)
                // }

                dataset.labels = Object.values(result[i].milestones)
                dataset.title = result[i]['title']
                dataset.colored = false;

                var btn_html = '<button class="ui button ' + (i === 0 ? 'active' : '') + '" data-attr="' + milestone_id + '">' + milestone_title + '</button>'
                $(id + ' .card-header .settings').append(btn_html)


                var chart = chart_linechart('#' + milestone_id, title, [dataset], '€', 'auto', 135)

                chart.options.myCustomOptions.datasets = []
                chart.options.myCustomOptions.datasets[0] = {}
                chart.options.myCustomOptions.datasets[0].milestone_values = Object.keys(result[i]['milestones'])
                chart.options.myCustomOptions.datasets[0].label = result[i].title
                chart.options.myCustomOptions.datasets[0].label_suffix = result[i].label_suffix

                chart = set_milestone_settings(chart);
                chart.update();
            }


        }
    });
}


$(document).ready(function () {
    setup();
    load_historical_data('#linechart', user_id, $('#linechart .settings button.active'), action = 'init', 'index')
    load_milestones('#milestones', 'Milestones')


    $('.toggleble_nav .item:first-child').addClass('active')
    $('.toggleble_nav_content .elem:first-child').removeClass('hidden')
    $(document).on('click', '.toggleble_nav .item', function () {
        let elem = $(this);

        let target = elem.attr('data-attr');

        set_active('.toggleble_nav .item', elem)

        $('.toggleble_nav_content .elem').addClass('hidden');
        $('.toggleble_nav_content .elem[data-attr=' + target + ']').removeClass('hidden');
    });

    $(document).on('click', '#linechart .settings button', function () {
        let elem = $(this);

        //set clicked btn active
        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

        load_historical_data('#linechart', user_id, $('#linechart .settings button.active'), action = 'update', 'index')
    });


    $(document).on('click', '#milestones .settings button', function () {
        let elem = $(this);
        let target = elem.attr('data-attr');

        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

        $('#milestones .card-body.main .tr_chart_container').addClass('hidden')


        var chart = get_instance_from_id(target + '_canvas')
        //chart = set_milestone_settings(chart);

        let data = chart.options.myCustomOptions.datasets[0].milestone_values.slice()
        chart.options.myCustomOptions.datasets[0].milestone_values = []

        $('#' + target).removeClass('hidden');
        setTimeout(function () {
            chart.options.myCustomOptions.datasets[0].milestone_values = data
            chart.update()
        }, 30);

    });

});
