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
        $('#' + col + '_' + data[col]).prop('selected', true);
    });

}

function serializeFormForDatabase(from_id) {
    //ToDo
}

$(document).ready(function () {

    $(document).on('click', '.edit_stock_button', function () {
        let portfolio_id = $(this).attr("portfolio_id");
        let asset_id = $(this).attr("asset_id");

        $.ajax({
            method: "POST",
            url: "/api/select_single_asset_from_portfolio/",
            data: {portfolio_id: portfolio_id, asset_id: asset_id},
            success: function (data) {
                data = data[0]
                console.log('data: ', data)

                let modal_id = '#edit_stock_modal'

                $(modal_id + "_label").text(data['title'] + ' - ' + data['symbol'])


                setFormValuesFromDatabase(modal_id, data)

                $(modal_id).modal('show');
            }
        });

    });


    $(document).on('click', '.edit_stock_button', function () {
        let portfolio_id = $(this).attr("portfolio_id");
        let asset_id = $(this).attr("asset_id");

        $.ajax({
            method: "POST",
            url: "/api/select_single_asset_from_portfolio/",
            data: {portfolio_id: portfolio_id, asset_id: asset_id},
            success: function (data) {

            }
        });

    });


});