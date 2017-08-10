$(".delete").click(function (e) {
        var id = $(this).data("id"),
            text = $(this).data("type");
        $.confirm({
            title: 'Confirmation!',
            content: 'Are you sure you want to delete this?',
            buttons: {
                confirm: function () {
                    $.ajax({
                        type: 'POST',
                        url: 'delete/',
                        data: {
                            "id": id,
                            "type": text
                        },
                        success: function (response) {
                            if (response == "done") {
                                $('table tr#' + id).remove();
                            }
                            else {
                                $.alert("Sorry we cant find the record");
                            }
                        },
                        failure: function () {
                            $.alert("Sorry this request cant be processed");
                        }
                    });
                },
                cancel: function () {
                }
            }
        });
    }
);

