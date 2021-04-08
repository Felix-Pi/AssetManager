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

function prepend_loader(id) {
    $(id).prepend('<div class="ui active loader"></div>')
}

function set_loader_active(id) {
    target = $(id + ' .loader');
    if (target === 'undefined') {
        prepend_loader(id);
    } else {
        $(id).find('.loader').addClass('active');
    }

}

function set_loader_inactive(id) {
    $(id).find('.loader').removeClass('active');
}

function set_active(elem_class, elem) {
    $(elem_class).removeClass('active');
    elem.addClass('active');
}


function load_newsfeed(symbol) {
    let id = '#newsfeed';
    set_loader_active(id);

    if ($(id) !== 'undefined') {
        $.ajax({
            method: "GET",
            url: "/api/render_template/",
            data: {'endpoint': 'default', 'action': 'get_news', 'symbol': symbol},
            success: function (result) {

                $(id).html(result);
                set_loader_inactive(id);
            }
        });
    }
}


$(document).ready(function () {
    $(document).on('click', '.accordion .title', function () { //ToDo: icon <
        let elem = $(this);
        let target = elem.parent().find('.content');

        target.slideToggle();
    });


    $(document).on('click', '#update_data', function (e, f) {
        $.ajax({
            method: "GET",
            url: "/api/refresh/",
            success: function (data) {
                console.log(data)
            }
        });
    });

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


