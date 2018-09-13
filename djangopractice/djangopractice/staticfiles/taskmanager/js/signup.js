var html = '<p class="alert alert-danger set_fixed_width"></p>';
var error = $('#errors');

function generate_error(id, message)
{
    var element = $(html).attr('id', id);
    var inner_html = element.append(message);
    error.append(inner_html);
}

$("#id_username").change(
    function () {
        var username = $(this).val();
        $.ajax({
            url: $('form').attr('data-validate-username-url'),
            data: {
                'username': username
            },
            dataType: 'json',
            success: function (data) {
                $('#error_username').remove();
                if (data.error_message) {
                    generate_error('error_username', data.error_message);
                }}
        });
    });

function validate_email(email)
{
    var pattern = /^[a-zA-Z0-9\-_]+(\.[a-zA-Z0-9\-_]+)*@[a-z]+(\-[a-z0-9]+)*(\.[a-z0-9]+(\-[a-z0-9]+)*)*\.[a-z]{2,4}$/;
    return pattern.test(email);
}

$("#id_email").change(
    function(){
        var email = $(this).val();
        $('#error_email').remove();
        if (!validate_email(email))
        {
            generate_error('error_email', "Email address is invalid");
        }
    }
);

$('#id_password1').change(
    function(){
        var password = $(this).val();
        $('#error_password').remove();
        if (password.length < 8)
        {
            generate_error('error_password', "Minimum Length of password is 8 characters");
        }
    });

$('#id_password2').change(
    function(){
        var password1 = $('#id_password1').val();
        var password2 = $(this).val();
        $('#error_match_password').remove();
        if (password1!=password2)
        {
            generate_error('error_match_password', "Password does not match Password Confirmation");
        }
    }
)

