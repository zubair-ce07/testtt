$(function () {
    
    
    $('.edit-blog').click(function (event) {
        event.preventDefault();
        console.log('Clicked');
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
                
            }
        });
    });
});
