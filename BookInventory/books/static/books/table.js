$(".delete").click(function () {
    var id = $(this).attr("id");
    var text = $(this).text();
    console.log(text);
    $.ajax({
        type: 'POST',
        url: 'delete/',
        data: {"id": id,
                "type":text
        },
        success: function (response) {
            if (response == "done") {
                $('table tr#'+id).remove();
            }
        }
    });
});