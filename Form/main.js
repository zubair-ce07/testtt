urls = {
    baseUrl: "http://127.0.0.1:8000/api",
    availableUsernamePassword: "/signup/available/",
    signup: "/signup/"
};

$(document).ready(function () {
    $username = $("input.username");
    $first_name = $("input.first_name");
    $last_name = $("input.last_name");
    $email = $("input.email");
    $password = $("input.password");
    $date_of_birth = $("input.date_of_birth");

    $username.on('keyup', function() {
        $("div.username").text("");
        $("div.username").html('<br>');
        $.ajax({
            data:{
                'username':$username.val()
            },
            type:"POST",
            url: urls.baseUrl+urls.availableUsernamePassword,
            dataType: 'text',
            success: function(data){
                displayAvailability(data, $username, 'username')
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    });

    $first_name.on('keydown', function() {
        $("div.first-name").text("")
        $("div.first-name").html('<br>')
    });

    $last_name.on('keydown', function() {
        $("div.last-name").text("")
        $("div.last-name").html('<br>')
    });

    $email.on('keyup', function () {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if(re.test($email.val()) == false && $email.val().length > 0) {
            $("div.email").text($email.val() + " is not a valid email address")
        } else {
            $("div.email").text("")
            $("div.email").html('<br>')
        }
        $.ajax({
            data:{
                'email':$email.val()
            },
            type:"POST",
            url: urls.baseUrl+urls.availableUsernamePassword,
            dataType: 'text',
            success: function(data){
                displayAvailability(data, $email, 'email')
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    });

    $password.on('keydown', function() {
        $("div.password").text("")
        $("div.password").html('<br>')
    });

    $("button").on('click', function (event) {
        event.preventDefault();
        raiseBlankField();
       $.ajax({
           data: {
               'username':$username.val(),
               'first_name':$first_name.val(),
               'last_name':$last_name.val(),
               'email':$email.val(),
               'password':$password.val(),
               'date_of_birth':$date_of_birth.val()
           },
           type: "POST",
           url: urls.baseUrl+urls.signup,
           dataType: 'text',
           success: function(data){
                   console.log(data)
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
       })
    });
});

var raiseBlankField = function(){
    $inputFields = $("input.input-field")
    for(let i = 0; i < $inputFields.length; i++){
        if($inputFields[i].value.length < 1){
            divName = getDivName($inputFields[i].name)
            $("div."+$inputFields[i].name.replace("_", "-")).text(divName+" can not be blank")
        }
    }
}

var getDivName = function(inputFieldName){
    divName = inputFieldName.replace("_", " ")
    return divName.replace(/\w\S*/g, function(txt){
        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    });
}

var displayAvailability = function(data, $handle, field){
    data = JSON.parse(data)
    if(data['is_taken'] === true){
        if(field == "username"){
            $("div."+field).text("Username " + $handle.val() + " is unavailable")
        } else {
            $("div."+field).text("Email Address " + $handle.val() + " is unavailable")
        }
    }
}
