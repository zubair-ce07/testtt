$(function () {

    $('.delete-blog').on('submit', function (event) {
        event.preventDefault();
        console.log();

        $.ajax({
            context: this,
            method: 'DELETE',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/' + $(this).find('.blog-slug').attr('value'),
            success: function (result) {
                console.log('Deleted');
                console.log(result);
                console.log($(this).parent('.blog-post'));
            }
        });
    });
});
