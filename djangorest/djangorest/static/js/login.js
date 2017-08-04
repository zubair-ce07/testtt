$(function () {

    $('.login-form').validate({
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true,
            }
        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password"
        },
        submitHandler: function (form) {
            var $login_form = $('.login-form');
            var csrf = $login_form.find("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/login/',
                contentType: "application/json; charset=utf-8",
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: JSON.stringify({
                    username: $login_form.find("input[name=username]").val(),
                    password: $login_form.find("input[name=password]").val(),
                }),
                success: function (result) {
                    window.location.replace("http://127.0.0.1:8000/blogs");
                    console.log(result);
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    $(".login-error").text(XMLHttpRequest.responseJSON['data']);
                }
            });
            return false;
        }

    });




    $('.register-form').validate({
        rules: {
            username: {
                required: true,
            },
            password1: {
                required: true,
            },
            password2: {
                required: true,
            },
            date_of_birth: {
                required: true,
                date: true,
            },
        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password",
        },
        submitHandler: function (form) {
            var $registration_form = $('.register-form');
            var csrf = $registration_form.find("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/signup/',
                contentType: "application/json; charset=utf-8",
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: JSON.stringify({
                    username: $registration_form.find("input[name=username]").val(),
                    password: $registration_form.find("input[name=password1]").val(),
                    profile: {
                        gender: $registration_form.find("select[name=gender]").val(),
                        address: $registration_form.find("input[name=address]").val(),
                        date_of_birth: $registration_form.find("input[name=date_of_birth]").val()
                    }
                }),
                success: function (result) {
                    console.log(result);
                    $(".message a").trigger("click");
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    if ("username" in XMLHttpRequest.responseJSON['data']) {
                        $(".register-error").text(XMLHttpRequest.responseJSON['data']['username']);
                    }
                }

            });
            return false;
        }
    });


    // Toogle Login and SignUp Form
    $('.message a').click(function () {
        $('form').animate({
            height: 'toggle',
            opacity: 'toggle'
        }, 'slow');
    });

});
