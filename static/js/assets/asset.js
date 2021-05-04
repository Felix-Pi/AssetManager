function setup_asset() {
    console.log('LOADED: asset.js')
    load_newsfeed(symbol);
}

$(document).ready(function () {
    setup_asset();

    //STOCK_NAVIGATION
    $(document).on('click', '#stock_navigation .item', function () {
        let elem = $(this);
        let target = elem.attr('data-attr');

        set_active('#stock_navigation .item', elem)

        $('#stock_navigation_content .elem').addClass('hidden');
        $('#stock_navigation_content .elem[data-attr=' + target + ']').removeClass('hidden');
    });


});