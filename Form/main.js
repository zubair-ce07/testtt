$(document).ready(function () {
    $username = $("input.username");
    $first_name = $("input.first_name");
    $last_name = $("input.last_name");
    $email = $("input.email");
    $password = $("input.password");
    $date_of_birth = $("input.date_of_birth");

    $username.on('keyup', function() {
        $("div.username").text("")
        $("div.username").html('<br>')
        $.ajax({
            data:{
                'username':$username.val()
            },
            type:"POST",
            url: 'http://127.0.0.1:8000/api/signup/available/',
            dataType: 'text',
            success: function(data){
                // console.log(data)
                display_availability(data, $username, 'username')
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    });

    $first_name.on('click', function () {
        RaiseBlankField(1)
    });

    $first_name.on('keydown', function() {
        $("div.first-name").text("")
        $("div.first-name").html('<br>')
    });

    $last_name.on('click', function () {
        RaiseBlankField(2)
    });

    $last_name.on('keydown', function() {
        $("div.last-name").text("")
        $("div.last-name").html('<br>')
    });

    $email.on('click', function () {
        RaiseBlankField(3)
        console.log(this)
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
            url: 'http://127.0.0.1:8000/api/signup/available/',
            dataType: 'text',
            success: function(data){
                // console.log(data)
                display_availability(data, $email, 'email')
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr.status);
                console.log(thrownError);
            }
        })
    });

    $password.on('click', function (event) {
        RaiseBlankField(4)
    });

    $password.on('keydown', function() {
        $("div.password").text("")
        $("div.password").html('<br>')
    });

    $date_of_birth.on('click', function (event) {
        RaiseBlankField(5)
    });

    $("button").on('click', function (event) {
        event.preventDefault();
        console.log("Button Clicked!", $username.val())
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
           url: 'http://127.0.0.1:8000/api/signup/',
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

var RaiseBlankField = function(inp){
    if(inp >= 1){
        if($username.val().length < 1){
            $("div.username").text("Username can not be blank")
        }
    }
    if(inp >= 2){
        if($first_name.val().length < 1){
            $("div.first-name").text("Name field can not be blank")
        }
    }
    if(inp >= 3){
        if($last_name.val().length < 1){
            $("div.last-name").text("Name field can not be blank")
        }
    }
    if(inp >= 4){
        if($email.val().length < 1){
            $("div.email").text("Email field can not be blank")
        }
    }
    if(inp >= 5){
        if($password.val().length < 1){
            $("div.password").text("Password can not be blank")
        }
    }
    if(inp >= 6){
        if($date_of_birth.val().length < 1){
            $("div.date-of-birth").text("Date can not be blank")
        }
    }
}

var display_availability = function(data, $handle, field){
    if(data=='true'){
        // console.log(":'3")
        if(field == "username"){
            $("div."+field).text("Username " + $handle.val() + " is unavailable")
        } else {
            $("div."+field).text("Email Address " + $handle.val() + " is unavailable")
        }
    }
}
