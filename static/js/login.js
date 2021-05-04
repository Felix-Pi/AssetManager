$('.form-group').each(function () {
    $(this).parent().html($(this).html())
})

$(document).on('click', '.main_message .close', function (e, f) {
    target = $(this).parent()
    target.fadeToggle()
    target.remove()
});
