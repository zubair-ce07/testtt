$(function () {
    $("#ajax-register-form").submit(function (event) {
        event.preventDefault();
    }).validate({
        rules: {
            username: {
                required: true
            },
            password1: {
                required: true
            },
            password2: {
                required: true
            },
            date_of_birth: {
                required: true,
                date: true
            },
            email: {
                email: true
            },
            phone_num: {
                maxlength: 15,
                minlength: 15
            },
            address: {
                maxlength: 150
            },

        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password",
            email: "Please enter a valid email address",
            phone_num: "Phone number cannot be greater or smaller than 15 digits",
            address: "Address cannot be greater than 150 charactors"
        },
        submitHandler: function (form) {
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/api/user/signup',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify($(form).serializeJSON()),
                success: function (result) {

                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {

                }
            });
            return false;
        }
    });
});
