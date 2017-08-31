const usernameExistUrl = "http://127.0.0.1:8000/user/username_exist/?username=",
 emailExistUrl = "http://127.0.0.1:8000/user/email_exist/?email=",
 emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/,
 onlyAlphabet = /^[A-Za-z ]+$/,
 emptyError = "*required",
 onlyAlphabetsError = "*only alphabets",
 alreadyExistError = "*already exist",
 passwordNotMatchedError = "password does not matched!",
 invalidEmailError = "*invalid email";

$(document).ready(function(){

    $("#id_first_name").blur(function () {
        $("#id_first_name").validate({
            pattern: onlyAlphabet,
            empty: function () {
                setError('id_first_name', emptyError);
            },
            invalid: function () {
                setError('id_first_name', onlyAlphabetsError);
            },
            valid: function () {
                hideErrorField('id_first_name');
            }
        });
        disableButton();
    });
    $("#id_last_name").blur(function () {
        $("#id_last_name").validate({
            pattern: onlyAlphabet,
            empty: function () {
                setError('id_last_name', emptyError);
            },
            invalid: function () {
                setError('id_last_name', onlyAlphabetsError);
            },
            valid: function () {
                hideErrorField('id_last_name');
            }
        });
        disableButton();
    });
    $("#id_username").blur(function(){
        var username = $("#id_username");
        username.validate({
            empty: function () {
                setError('id_username', emptyError);
            }
        });
        username.isExist({
            url: usernameExistUrl,
            exist: function () {
                setError('id_username', alreadyExistError);
            },
            notExist: function () {
                hideErrorField('id_username');
            }
        });
        disableButton();
    });
    $("#id_email").blur(function(){
        var email = $("#id_email");
        email.validate({
            pattern: emailPattern,
            empty: function () {
                setError('id_email', emptyError);
            },
            invalid: function () {
                setError('id_email', invalidEmailError);
            }
        });
        email.isExist({
            url: emailExistUrl,
            exist: function () {
                setError('id_email', alreadyExistError);
            },
            notExist: function () {
                hideErrorField('id_email');
            }
        });
        disableButton();
    });
    $("#id_confirm_password").blur(function () {
        $("#id_confirm_password").equalTo({
            id: "#id_password",
            notEqual: function () {
                setError('id_confirm_password', passwordNotMatchedError);
            },
            equal: function () {
                hideErrorField('id_confirm_password');
            }
        });
        disableButton();
    });
    $("#id_country").blur(function () {
        $("#id_country").validate({
            pattern: onlyAlphabet,
            empty: function () {
                setError('id_country', emptyError);
            },
            invalid: function () {
                setError('id_country', onlyAlphabetsError);
            },
            valid: function () {
                hideErrorField('id_country');
            }
        });
        disableButton();
    });
    $("#id_state").blur(function () {
        $("#id_state").validate({
            pattern: onlyAlphabet,
            empty: function () {
                setError('id_state', emptyError);
            },
            invalid: function () {
                setError('id_state', onlyAlphabetsError);
            },
            valid: function () {
                hideErrorField('id_state');
            }
        });
        disableButton();
    });
    $("#id_city").blur(function () {
        $("#id_city").validate({
            pattern: onlyAlphabet,
            empty: function () {
                setError('id_city', emptyError);
            },
            invalid: function () {
                setError('id_city', onlyAlphabetsError);
            },
            valid: function () {
                hideErrorField('id_city');
            }
        });
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
            //if (isvisible($("#id_"+fieldNames[i]+"_error"))){
            btnSubmit.prop('disabled', true);
            return;
        }
    }
    btnSubmit.prop('disabled', false);
}

