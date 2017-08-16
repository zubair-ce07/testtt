$(function () {

    $('.delete-blog').on('submit', function (event) {
        event.preventDefault();

        $.ajax({
            context: this,
            method: 'DELETE',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/' + $(this).find('.blog-slug').attr('value'),
            complete: function () {
                $(this).parent('.blog-post').hide('slow', function () {
                    $(this).remove();
                });
                $('#content1 a[href=' + $(this).find('.blog-slug').attr('value') + ']').parents('.blog-post').hide('slow', function () {
                    $(this).remove();
                });
            }
        });
    });
});
