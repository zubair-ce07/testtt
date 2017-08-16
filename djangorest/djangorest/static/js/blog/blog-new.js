$(function () {

    $('.submit-blog').on('submit', function (event) {
        event.preventDefault();
        
        console.log($(this).serializeJSON({checkboxUncheckedValue: "false"}));
        
        $.ajax({
            context: this,
            method: 'POST',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/',
            data: $(this).serializeJSON({checkboxUncheckedValue: "false"}),
            success: function (result) {
                this.reset();
                add_user_blog(result);
                if (result.is_public && result.is_published) {
                    add_published_blog(result);
                }
            }
        });
    });
});
