const usernameExistUrl = "http://127.0.0.1:8000/user/username_exist/?username=",
    emailExistUrl = "http://127.0.0.1:8000/user/email_exist/?email=",
    emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
    onlyAlphabet = /^[A-Za-z ]+$/,
    emptyError = "cannot be empty",
    onlyAlphabetsError = "*only alphabets",
    alreadyExistError = "*already exist!",
    passwordNotMatchedError = "Password does not matched!",
    invalidEmailError = "Invalid Email";

$(document).ready(function(){

    $("#id_first_name").blur(function () {
        validate('first_name');
        disableButton();
    });
    $("#id_last_name").blur(function () {
        validate('last_name');
        disableButton();
    });
    $("#id_username").blur(function(){
        var username = $("#id_username").val();
        if (username === "")
            setError('id_username', emptyError);
        else
            isExist(username, 'username');
        disableButton();
    });
    $("#id_email").blur(function(){
        var email = $("#id_email").val();
        if ((!emailPattern.test(email)))
            setError('id_email', invalidEmailError);
        else
            isExist(email, "email");
        disableButton();
    });
    $("#id_confirm_password").blur(function () {
        var confirmPassword = $("#id_confirm_password").val();
        var password = $("#id_password").val();
        if (!(password === confirmPassword))
            setError('id_confirm_password', passwordNotMatchedError);
        else
            hideErrorField('id_confirm_password');
        disableButton();
    });
    $("#id_country").blur(function () {
        validate("country");
        disableButton();
    });
    $("#id_state").blur(function () {
        validate("state");
        disableButton();
    });
    $("#id_city").blur(function () {
        validate("city");
        disableButton();
    });

    (function s() {
        var fieldNames = [
            "first_name", "last_name", "username",
            "email", "confirm_password", "country",
            "state", "city"
        ];
        for (var i=0; i<fieldNames.length; i++){
            $("#id_"+fieldNames[i]+"_error").hide();
        }
    })();

});

function isExist(value, fieldName) {
    var url = emailExistUrl;
    if (fieldName==='username')
        url = usernameExistUrl;

    $.get(url+value, function (response) {
        if (response.status === true)
            setError('id_'+fieldName, alreadyExistError);
        else
            hideErrorField('id_'+fieldName);
    });
}

function validate(fieldName) {
    var value = $("#id_"+fieldName).val();
    if (value ==="")
        setError('id_'+fieldName, emptyError);
    else if (!onlyAlphabet.test(value))
        setError('id_'+fieldName, onlyAlphabetsError);
    else
        hideErrorField('id_'+fieldName);
}

function setError(elementId, errorMessage) {
    var element = $("#"+elementId+"_error");
    element.show();
    element.text(errorMessage);
}

function hideErrorField(elementId) {
    var element = $("#"+elementId+"_error");
    element.hide();
    element.text("");
}

function disableButton (){
    var btnSubmit = $(':input[type="submit"]');
    var fieldNames = [
        "first_name", "last_name", "username",
        "email", "confirm_password", "country",
        "state", "city"
    ];
    for (var i=0; i<fieldNames.length; i++){
        if ($("#id_"+fieldNames[i]+"_error").is(":visible") === true){
            btnSubmit.prop('disabled', true);
            return;
        }
    }
    btnSubmit.prop('disabled', false);
}

