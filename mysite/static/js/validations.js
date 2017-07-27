function verifyUserName(e)
{
    var username = e.target.value;
    if(username)
    {
        $.ajax({
            url: "/validate_username/",
            type: "GET",
            data: {
              'username': username
            },
            success: function(result){
                console.log("Success");
                e.target.className = "form-control success"
            },
            error: function (HttpRequest, textStatus, errorThrown) {
                console.log("Error: " + errorThrown);
                e.target.className = "form-control error"
            }
        });
    }
    else
    {
        console.log("Error: Username empty");
        e.target.className = "form-control error"
    }
}

function verifyName(e)
{
    var name = e.target.value;
    var charCode = e.charCode;

    if((charCode>=65 && charCode<=90) || (charCode>=97 && charCode<=122))
    {
        if(name.length >= 10)
        {
            e.returnValue = false;
        }
        return true;
    }
    return false;
}
