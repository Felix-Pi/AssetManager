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


});