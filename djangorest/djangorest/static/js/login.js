$(function () {
    // Toogle Login and SignUp Form
    $('.message a').click(function () {
        $('form').animate({
            height: 'toggle',
            opacity: 'toggle'
        }, 'slow');
    });

    //Login Request
    $(".login-form").submit(function (event) {
        event.preventDefault();
        $.post('http://127.0.0.1:8000/login/',
            $(this).serialize()
        ).done(function (data) {
            window.location.replace("http://127.0.0.1:8000/blogs");
        });
    });

    //Signup Request
    $(".register-form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            method: 'POST',
            dataType: 'json',
            url: 'http://127.0.0.1:8000/signup/',
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", $("input[name=csrfmiddlewaretoken]").val());
            },
            data: JSON.stringify({
                username: $("input[name=username]").val(),
                password: $("input[name=password1]").val(),
                profile: {
                    gender: $("select[name=gender]").val(),
                    address: $("input[name=address]").val(),
                    date_of_birth: $("input[name=date_of_birth]").val()
                }
            }),
            success: function (result) {
                $(".message a").trigger("click");
            }
        });
    });
});
