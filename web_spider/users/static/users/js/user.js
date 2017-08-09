(function (window){

    function User(email, password, confirmPassword, firstName, lastName, dob, photo, errorList){
        this.firstName = firstName;
        this.lastName = lastName;
        this.confirmPassword = confirmPassword;
        this.dob = dob;
        this.photo = photo;
        this.email = email;
        this.password = password;
        // UL element in DOM where output is to be shown
        this.errorList = errorList;
    }

    User.prototype.validateEmail = function () {
        var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(this.email);
    };

    User.prototype.validatePassword = function () {
        return this.password === this.confirmPassword;

    };

    User.prototype.validateDob = function () {
        var dateStr = Date.parse(this.dob);
        return !isNaN(dateStr)
    };

    User.prototype.isValid = function (callback) {
        var validFlag = true;
        this.errorList.empty();
        $('#json').empty();

        if(!this.validateEmail()) {
            this.errorList.append($('<li></li>').text('Enter a valid Email.'));
            validFlag = false;
        }
        if(!this.validateDob()){
            this.errorList.append($('<li></li>').text('Date of birth is required. Use MM-DD-YYYY format'));
            validFlag = false;
        }
        if(callback === undefined){
            return validFlag;
        }

        if(this.password === ''){
            this.errorList.append($('<li></li>').text('Password is required.'));
            validFlag = false;
        }
        if(!this.validatePassword()){
            this.errorList.append($('<li></li>').text('Password does not match with Confirm Password.'));
            validFlag = false;
        }

        if($('#photo')[0].files.length){
            var photo = this.photo[0].files[0],
            img = new Image(),
            errorList = this.errorList,
            boundCallback = callback.bind(this); // callback used to save user is bound to this context

            img.onload = function() {
                var ratio = this.width/this.height;
                if(ratio < 0.8 || ratio > 1.5) {
                    errorList.append($('<li></li>').text('Aspect ratio should be greater than 1 and less than 1.5'));
                    validFlag = false;
                }
                if(validFlag) {
                    boundCallback();
                }
            };

            img.onerror = function() {
                errorList.append($('<li></li>').text('Choose an image file.'));
                validFlag = false;
            };

            img.src = window.URL.createObjectURL(photo);
        }
    };


    User.prototype.createUser = function () {
        // if data is valid then callback is called to create user
        this.isValid(this.createValidatedUser)
    };

    User.prototype.createValidatedUser = function () {
        var errors = this.errorList,
        formData = new FormData();
        $('progress').show();

        if(this.photo[0].files.length) {
            formData.append('photo', this.photo[0].files[0]);
        }

        formData.append('email', this.email);
        formData.append('first_name', this.firstName);
        formData.append('last_name', this.lastName);
        formData.append('date_of_birth', this.dob);
        formData.append('password', this.password);
        formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());

        $.ajax({
            method: 'POST',
            url: '/api/users/',
            data: formData,
            cache: false,
            contentType: false,
            processData: false,
            xhr: manageProgress,
            success: function () {
                $('#success').text('User Created.');
            },
             error: function (xhr) {
                 errorInAjax(xhr, errors);
             }
        });
    };

    function manageProgress() {
        var myXhr = $.ajaxSettings.xhr();
        if (myXhr.upload) {
            // For handling the progress of the upload
            myXhr.upload.addEventListener('progress', function(e) {
                if (e.lengthComputable) {
                    $('progress').attr({
                        value: e.loaded,
                        max: e.total
                    });
                }
            } , false);
        }
        return myXhr;
    }

    User.prototype.load = function (userId, errors) {
        errors.empty();

        $.ajax({
            method: 'GET',
            url: '/api/users/' + userId + '/',
            success: function (data) {
                $('#email').val(data.email);
                $('#f_name').val(data.first_name);
                $('#l_name').val(data.last_name);
                $('#dob').val(data.date_of_birth);
                $('#photo').attr('src', data.photo);
            },
             error: function (xhr) {
                 errorInLoad(xhr, errors);
             }
        });
    };

    User.prototype.deleteUser = function (userId, errors) {
        errors.empty();

        $.ajax({
            headers: {
                'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
            },
            method: 'DELETE',
            url: '/api/users/' + userId + '/',
            success: function () {
                $('#success').text('User deleted.');
                window.location.href = '/login/'
            },
            error: function (xhr) {
                errorInLoad(xhr, errors);
            }
        });
    };

    function errorInLoad(xhr, errors) {
        if(xhr.status === 0)
            errors.append($('<li></li>').text('Error Occurred: Check your internet connectivity.'));
        else if(xhr.status === 403 || xhr.status === 401 || xhr.status === 400)
            errors.append($('<li></li>').text(xhr.responseJSON.detail));
        else if(xhr.status === 404) {
            $('#details').hide();
            errors.append($('<li></li>').text('Requested Page not found.'));
        }
     }

    User.prototype.updateUser = function (userId) {
        if(this.isValid()){
            var errors = this.errorList;
            $.ajax({
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                type: 'PATCH',
                url: '/api/users/' + userId + '/',
                data: {
                    email: this.email,
                    first_name: this.firstName,
                    last_name: this.lastName,
                    date_of_birth: this.dob
                },
                success: function () {
                    $('#success').text('User Updated.');
                },
                 error: function (xhr) {
                     errorInAjax(xhr, errors);
                 }
            });
        }
    };

    function errorInAjax(xhr, errors) {
        if(xhr.status === 0)
            errors.append($('<li></li>').text('Error Occurred: Check your internet connectivity.'));
        else if(xhr.status === 403 || xhr.status === 401 || xhr.status === 400) {
            var msg = JSON.stringify(xhr.responseJSON, undefined, 2);
            msg = msg.replace(/[\[\]"{}]+/g, '');
            $('#json').text(msg);
        }
    }

    window.User = User;
}(window));
