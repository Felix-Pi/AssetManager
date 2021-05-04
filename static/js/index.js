function setup() {
    load_newsfeed(all_symbols);
    /* setup stock distribution */
    let USER_ID = 1 //todo
    $.ajax({
        url: "/api/index/"+ USER_ID +"/asset_distribution",
        success: function (result) {
            var id = '#asset_distribution'

            result.data = result.data_relative;
            result.colored = true;

            asset_distribution_chart = chart_half_doughnut(id, 'Asset distribution', result, '%', 'auto', 150)


        }
    });

    $.ajax({
        url: "/api/index/"+ USER_ID +"/monthly_transactions",
        success: function (result) {
            var id = '#monthly_transactions'

            result.data = result.data_absolute;
            result.colored = true;
            title = 'Monthly Payments:~<i class=\'icon ban rotated\'></i>' + result['average'] + ' € per month'

            console.log(result)

            monthly_transactions_chart = bar_chart(id, title, result, '€', 'auto', 150)


        }
    });
}

$(document).ready(function () {
    setup();

    $('.toggleble_nav .item:first-child').addClass('active')
    $('.toggleble_nav_content .elem:first-child').removeClass('hidden')
    $(document).on('click', '.toggleble_nav .item', function () {
        let elem = $(this);

        let target = elem.attr('data-attr');

        set_active('.toggleble_nav .item', elem)

        $('.toggleble_nav_content .elem').addClass('hidden');
        $('.toggleble_nav_content .elem[data-attr=' + target + ']').removeClass('hidden');
    });
});