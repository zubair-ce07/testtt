function validateEmail(email) {
    var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(email);
}

function validateForm() {
    var email = document.forms["update_profile"]["email"].value;
    if (!validateEmail(email)) {
        $("#email_div").addClass("has-error");
        $("#email_error").text("Invalid Email").css("color", "red");
        return false;
    }
}
