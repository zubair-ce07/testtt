/* TOKEN Variables */
var TOKEN = null;
var USERNAME = null;


$(function () {
    /* Form Validation and Submittion */
    $("#ajax-login-form").submit(function (event) {
        event.preventDefault();
    }).validate({
        rules: {
            username: {
                required: true
            },
            password: {
                required: true
            }
        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password"
        },
        submitHandler: function (form) {
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/api-token-auth/',
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify($(form).serializeJSON()),
                success: function (result) {
                    /* Initializing Token */
                    TOKEN = result.token;
                    USERNAME = $(form).find('input[name=username]').val();
                    $('.alert-login').show().fadeTo(3000, 0).slideUp(200, function () {
                        $(this).remove();
                    });
                    init();
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    $("#invalid-credentials").text("Invalid Credentials");
                }
            });
            return false;
        }
    });


});
