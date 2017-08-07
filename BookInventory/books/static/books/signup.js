function validateForm() {
    var password = $("#password").val();
    var re_password = $("#re-password").val();
    if ($("#username").val() == "") {
        $("#username_error").text("You can't have empty username")
        return false;
    }
    if (password == "") {
        $("#password_error").text("You can't have empty Password");
        return false;
    }
    else if (password != re_password) {
        $("#password_error").text("Passwords Doesn't match");
        $("#password").val("");
        $("#re-password").val("");
        return false;
    }
    else if (password.length < 6) {
        $("#password_error").text("Password is too short, Enter atleast 6 characters");
        $("#password").val("");
        $("#re-password").val("");
        return false;
    }
}