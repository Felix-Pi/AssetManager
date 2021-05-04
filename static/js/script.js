function setFormValuesFromDatabase(form_id, data) {
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
        var key = elem.attr('col');

        if (elem.attr('type') === 'number') {
            key = key.replaceAll(',', '.');
        }

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


/**
 * prepends loader div to html element
 * @param id html id
 */
function prepend_loader(id) {
    $(id).prepend('<div class="ui active loader"></div>')
}

/**
 * sets loader div active
 * @param id html id
 */
function set_loader_active(id) {
    target = $(id + ' .loader');
    if (target === 'undefined') {
        prepend_loader(id);
    } else {
        $(id).find('.loader').addClass('active');
    }

}

/**
 * sets loader div inactive
 * @param id html id
 */
function set_loader_inactive(id) {
    $(id).find('.loader').removeClass('active');
}

/**
 * sets loader div active
 * @param id html id
 */
function add_spinner(id) {
    target = $(id);

    console.log($(id + ' .spinner'))
    if ($(id + ' .spinner').length == 0) {
        target.append('<i class="fas spinner fa-spinner fa-spin"></i>')
    }
}

/**
 * sets loader div inactive
 * @param id html id
 */
function remove_spinner(id) {
    $(id + ' .spinner').remove()
}


/**
 * sets html element active, removes other active elements for this target
 * @param elem_class html class or object
 * @param elem html class or object
 */
function set_active(elem_class, elem) {
    $(elem_class).removeClass('active');
    elem.addClass('active');
}


/**
 * loads newsfeed for symbol(s)
 * @param symbol or comma separated list of symbols
 */
function load_newsfeed(symbol) {
    let id = '#newsfeed';
    set_loader_active(id);

    if ($(id) !== 'undefined') {
        $.ajax({
            method: "GET",
            url: '/api/render_template/news/' + symbol,
            success: function (result) {
                $(id).html(result);
                set_loader_inactive(id);
            }
        });
    }
}

/**
 * load html content from webserver and insert to html
 * @param id html id
 * @param endpoint url
 * @param data Object. ex: data: {'endpoint': 'default', 'action': 'get_news', 'symbol': symbol},
 */
function load_content(id, endpoint, data) {
    set_loader_active(id);

    $.ajax({
        method: "GET",
        url: endpoint,
        //data: {'endpoint': 'default', 'action': 'get_news', 'symbol': symbol},
        data: data,
        success: function (result) {
            $(id).html(result);
        },
        error: function (result) {
            $(id).html(result);
            $(id).prepend('<p>Could not load content!</p>');
        }
    });

    set_loader_inactive(id);
}

function load_historical_data(id, symbol, elem) {
    $.ajax({
        url: "/api/asset/" + symbol + "/historical_data",
        data: {
            'period': elem.attr('data-period'),
            'interval': elem.attr('data-interval'),
        },
        success: function (result) {
            result = JSON.parse(result)

            result.median = Object.values(result['Median'])
            result.labels = Object.values(result['timestamps'])
            result.colored = false;

            $(id).attr('data-symbol', symbol)


            linechart = chart_linechart(id, 'Line chart', [result], '€')
            $(id + ' .card-header span').text(title + ': ' + price);
        }
    });
}

$(document).ready(function () {
    $('.ui.dropdown').dropdown();


    //MAIN_NAVIGATION
    $(document).on('click', '.main_navigation .item', function () {
        let elem = $(this);

        if (!elem.hasClass('dropdown')) {
            let target = elem.attr('data-attr');

            set_active('.main_navigation .item', elem)

            $('.main_navigation_content .elem').addClass('hidden');
            $('.main_navigation_content .elem[data-attr=' + target + ']').removeClass('hidden');
        }
    });

    /**
     * accordeon logic
     */
    $(document).on('click', '.accordion .title', function () { //ToDo: icon
        let elem = $(this);
        let target = elem.parent().find('.content');

        target.slideToggle();
    });


    /**
     * call update_data() to refresh data
     */
    $(document).on('click', '#update_data_price', function (e, f) {
        add_spinner('#update_data_price')
        $.ajax({
            method: "GET",
            url: "/api/update_data_price",
            success: function (data) {
                remove_spinner('#update_data_price')
            }
        });
    });

    $(document).on('click', '#update_data_full', function (e, f) {
        add_spinner('#update_data_full')
        $.ajax({
            method: "GET",
            url: "/api/update_data_full",
            success: function (data) {
                remove_spinner('#update_data_full')
            }
        });
    });
    $(document).on('click', '#update_all_positions', function (e, f) {
        add_spinner('#update_all_positions')
        $.ajax({
            method: "GET",
            url: "/api/update_all_positions",
            success: function (data) {
                remove_spinner('#update_all_positions')
            }
        });
    });


    $(document).on('click', '.main_message .close', function (e, f) {
        target = $(this).parent()
        target.fadeToggle()
        target.remove()
    });


    /**
     * settings buttons for .card
     */
    $(document).on('click', '.card .settings button', function (e, f) {
        let elem = $(this);
        let chart_type = elem.attr('chart-type');


        set_active(elem.parent().find('.active'), elem);

        if (elem.hasClass('change_chart_type')) {
            let target = elem.parent().parent().parent().find('.card-body');
            let chart_id = target.find('canvas').attr('id').toString();


            if (chart_type === 'bar') {
                elem.find('i').removeClass('fa-chart-bar').addClass('fa-chart-pie');
            }
            if (chart_type === 'doughnut' || chart_type === 'pie') {
                elem.find('i').removeClass('fa-chart-pie').addClass('fa-chart-bar');
            }

            let chart = get_instance_from_id(chart_id)
            change_chart_type(chart);
        }

    });


    $(document).on('click', '.card .more', function (e, f) {
        elem = $(this)
        elem.parent().parent().parent().find('.card-footer').slideToggle()

    });

    /* search box: search yahoo finance */
    $(document).on('input', '#searchbar', function () {
        elem = $('#searchbar');

        $('#searchbar_results').show()
        $('#searchbar_results').html('')

        $.ajax({
            method: "GET",
            url: '/api/stock/yahoo_search/',
            data: {'input': elem.val()},
            success: function (data) {
                data = JSON.parse(data);
                data = data['ResultSet']['Result'];
                for (let i = 0; i < data.length; i++) {
                    var item = data[i]
                    html = '' +
                        '<a class="result" href="https://de.finance.yahoo.com/quote/' + item['symbol'] + '" target="_blank">' +
                        '   <div class="content">' +
                        '       <div class="title">' + item['name'] + '</div>' +
                        '       <div class="description">' + item['symbol'] + ' - ' + item['exch'] + '</div>' +
                        '   </div>' +
                        '</a>'
                    $('#searchbar_results').append(html)
                }

            }
        });

    });
    /*
    toggle profit label
     */

    $('.profit_label').each(function () {
        elem = $(this)

        console.log(elem)
        profit_val = parseFloat(elem.text())

        elem_text = elem.find('.label').find('span')

        suffix = ' €'

        if (profit_val < 0) {
            profit_val = profit_val * (-1)
            elem_text.text('  ' + profit_val)
        }

        elem_text.append(suffix)
    });

    const zeroPad = (num, places) => String(num).padStart(places, '0')

    $(document).on('click', '.profit_label', function () { //ToDo fix
        $('.profit_label').each(function () {
            let elem = $(this)

            let counter = parseInt(elem.attr('counter'))
            let content = elem.attr('data-val').split('~')
            let suffix_list = ['%', '€', '%', '€'];

            var suffix = suffix_list[counter];

            if (counter === content.length - 1) {
                counter = 0
            } else {
                counter += 1
            }


            var content_val = parseFloat(content[counter]);
            content_val = zeroPad(content_val, 2)


            if (content_val > 0) {
                var color = 'green'
                var icon = 'fas fa-caret-up'
            } else {
                var color = 'red'
                var icon = 'fas fa-caret-down'
                content_val = content_val * (-1)
            }

            let target_elem = elem.find('.label')


            target_elem.removeClass('.red .green')
            target_elem.addClass(color)


            elem.attr('counter', counter)
            target_elem.html('<i class="' + icon + '"></i> ' + content_val + ' ' + suffix);

            profit_label_titles = ['profit total', ' profit today', 'profit today', 'profit total']
            $('#profit_label_title').text(profit_label_titles[counter])

        });
    });
});


