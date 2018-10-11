function login(event)
{
	document.getElementById('login_error').innerHTML = "";
    let username = document.getElementById("login_username").value;
    let password = document.getElementById("login_password").value;
    
	fetch(`http://localhost:3000/users?username=${username}`)
	.then(response => response.json())
	.then(user_list => 
	{
        if(user_list.length && user_list[0].password == password)
        {
            sessionStorage.setItem("loggedin_user", JSON.stringify(user));
	 		window.location.replace('home.html');
        }
        else
        	document.getElementById('login_error').innerHTML = " ** Invalid username or password";
	})
	.catch(alert)
	
	return false;
}