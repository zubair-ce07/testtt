const usernameExistUrl = "http://127.0.0.1:8000/user/username_exist/?username=",
    emailExistUrl = "http://127.0.0.1:8000/user/email_exist/?email=",
    emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
    onlyAlphabet = /^[A-Za-z ]+$/,
    emptyError = "cannot be empty",
    onlyAlphabetsError = "*only alphabets",
    alreadyExistError = "*already exist!",
    passwordNotMatchedError = "Password does not matched!",
    invalidEmailError = "Invalid Email";


window.onload = function() {

    const firstName = document.getElementById('id_first_name'),
        lastName = document.getElementById('id_last_name'),
        username = document.getElementById('id_username'),
        email = document.getElementById('id_email'),
        password = document.getElementById('id_password'),
        confirmPassword = document.getElementById('id_confirm_password'),
        country = document.getElementById('id_country'),
        state = document.getElementById('id_state'),
        city = document.getElementById('id_city'),
        form = document.getElementById('form');

    firstName.onblur = function () {
        validate('first_name', firstName.value);
        disableButton();
    };
    lastName.onblur = function () {
        validate('last_name', lastName.value);
        disableButton();
    };
    username.onblur = function () {
        if (username.value === "")
            setError('id_username', emptyError);
        else
            isExist('username', username.value);
        disableButton();
    };
    email.onblur = function () {
        if (!emailPattern.test(email.value))
            setError('id_email', invalidEmailError);
        else
            isExist('email', email.value);
        disableButton();
    };
    confirmPassword.onblur = function () {
        if (!(password.value === confirmPassword.value))
            setError('id_confirm_password', passwordNotMatchedError);
        else
            hideErrorField('id_confirm_password');
        disableButton();
    };
    country.onblur = function () {
        validate('country', country.value);
        disableButton();
    };
    state.onblur = function () {
        validate('state', state.value);
        disableButton();
    };
    city.onblur = function () {
        validate('city', city.value);
        disableButton();
    }
};

function validate(fieldName, value) {
    if (value ==="")
        setError('id_'+fieldName, emptyError);
    else if (!onlyAlphabet.test(value))
        setError('id_'+fieldName, onlyAlphabetsError);
    else
        hideErrorField('id_'+fieldName);
}

function isExist(fieldName, username) {
    var url = emailExistUrl;
    if (fieldName ==='username')
        url = usernameExistUrl;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange=function() {
        if (this.readyState === 4 && this.status === 200) {
            if (this.response.status === true) {
                setError('id_'+fieldName, alreadyExistError);
            }else
                hideErrorField('id_'+fieldName)
        }
    };
    xhttp.open("GET", url+username, true);
    xhttp.send();
}

function setError(elementId, errorMessage) {
    var errorField = document.getElementById(elementId+"_error");
    errorField.style.visibility = 'visible';
    errorField.innerHTML = errorMessage;
}

function hideErrorField(elementId) {
    var errorField = document.getElementById(elementId+"_error");
    errorField.innerHTML = "";
    errorField.style.visibility = 'hidden';
}

function disableButton(){
    const btnSubmit = document.getElementById("id_submit");
    var fieldNames = [
        "first_name", "last_name", "username",
        "email", "confirm_password", "country",
        "state", "city"
    ];
    for (var i=0; i<fieldNames.length; i++){
        var errorField = document.getElementById("id_"+fieldNames[i]+"_error");
        if (isvisible(errorField)){
            btnSubmit.disabled = true;
            return;
        }
    }
    btnSubmit.disabled = false;
}

function isvisible(errorField) {
    return errorField.offsetWidth > 0 && errorField.offsetHeight > 0;
}
