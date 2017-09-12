$(function () {

    $('.comment-new').on('submit', function (event) {
        event.preventDefault();
        console.log($(this).serializeJSON());

        $.ajax({
            context: this,
            method: 'POST',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/comment/',
            data: $(this).serializeJSON(),
            success: function (result) {
                add_comment(result);
            }
        });
    });
});
