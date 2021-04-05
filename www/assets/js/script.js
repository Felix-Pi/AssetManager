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

$(document).ready(function () {

    $('.ui.accordion').accordion();

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
        elem = $(this)

        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

    });
    $(document).on('click', '.card .settings button', function (e, f) {
        elem = $(this)

        elem.parent().find('.active').removeClass('active');
        elem.addClass('active');

    });

    $(document).on('click', '.card .more', function (e, f) {
        elem = $(this)
        console.log('elemmm', elem.parent().parent().find('.card-footer'))
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
                console.log(data)
                for (let i = 0; i < data.length; i++) {
                    var item = data[i]
                    console.log(item)
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

    $(document).on('click', '.profit_label', function () {
        $('.profit_label').each(function () {
            let elem = $(this)

            let counter = parseInt(elem.attr('counter'))
            let content = elem.attr('data-val').split('~')

            if (counter < 1) {
                suffix = ' €'
            } else {
                suffix = ' %'
            }

            if (counter === content.length - 1) {
                counter = 0
                suffix = ' €'
            } else {
                counter += 1
            }


            let content_val = parseFloat(content[counter])
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
            target_elem.html('<i class="' + icon + '"></i> ' + content_val + suffix)

            profit_label_titles = ['profit total', 'profit total', ' profit today', 'profit today']
            $('#profit_label_title').text(profit_label_titles[counter])

        });
    });
});


