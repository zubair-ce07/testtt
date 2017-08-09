(function(window){
    function Login(email, password, errorList){
        this.email = email;
        this.password = password;
        this.errorList = errorList;
    }

    Login.prototype.validateEmail = function () {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(this.email);
    };

    Login.prototype.validatePassword = function () {
        return this.password !== "";
    };

    Login.prototype.isValid = function () {
        var validFlag = true;
        this.errorList.empty();

        if(!this.validateEmail()) {
            this.errorList.append($('<li></li>').text('Enter a valid Email.'));
            validFlag = false;
        }
        if(!this.validatePassword()){
            this.errorList.append($('<li></li>').text('Password is required.'));
            validFlag = false;
        }
        return validFlag;
    };

    Login.prototype.signIn = function () {
        if(this.isValid()){
            var errors = this.errorList;
            $.ajax({
                method: 'POST',
                url: '/api/login/',
                data: {
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                    email: this.email,
                    password: this.password
                },
                success: function (data) {
                    $('#success').text('Login successful for ' + data.email + '. Redirecting ...');
                    localStorage.setItem("user_id", data.id);
                    window.location.href = '/users/'
                },
                 error: function (xhr) {
                    if(xhr.status === 0)
                        errors.append($('<li></li>').text('Error Occurred: Check your internet connectivity.'));
                    else if(xhr.status === 403 || xhr.status === 401 || xhr.status === 400)
                    errors.append($('<li></li>').text(xhr.responseJSON.detail))
                 }
            });
        }
    };

    window.Login = Login;
}(window));
