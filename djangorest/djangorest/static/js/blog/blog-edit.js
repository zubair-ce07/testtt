$(function () {
    
    
    $('.edit-blog').click(function (event) {
        event.preventDefault();
        $(this).parent().find('textarea').removeAttr('readonly');
    });
    

    $('.edit-blog-form').on('submit', function (event) {
        event.preventDefault();
    
        $.ajax({
            context: this,
            method: 'PUT',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/' + $(this).attr('name') + '/',
            data: $(this).serializeJSON({checkboxUncheckedValue: "false"}),
            success: function (result) {
                if (result.is_public && result.is_published) {
                    add_published_blog(result);
                }
            }
        });
    });
});
