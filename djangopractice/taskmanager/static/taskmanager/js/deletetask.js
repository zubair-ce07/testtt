// Function getCookie taken from Django Documentation
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(".js-delete-task").click(
    function(){
        $(".js-task-delete-button").val($(this).val())
        $("#modal-task").modal('show');
    });

$(".js-task-delete-button").click(
    function(){
        var id = $(".js-task-delete-button").val();
        $.ajax({
            url: $('#delete_task').attr('data-delete-task-url'),
            type: 'POST',
            data: {
                'pk': id
            },
            dataType: 'json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                $("#modal-task").modal('hide');
            },
            success: function (data) {
                if(data.valid)
                {
                    $('#row_' + id).remove();
                }
            }
        });
    }
);
