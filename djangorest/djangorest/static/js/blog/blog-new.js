$(function () {

    $('.submit-blog').on('submit', function (event) {
        event.preventDefault();
        console.log($(this).serializeJSON());

        $.ajax({
            context: this,
            method: 'POST',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/',
            data: $(this).serializeJSON(),
            success: function (result) {
                console.log(result);
                add_published_blog(result);
                add_user_blog(result);
            }
        });
    });
});
