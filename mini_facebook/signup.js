function saveUser(user)
{
	let user_list = localStorage.getItem("user_list");
	if(!user_list)
		user_list = [];
	else 
		user_list = JSON.parse(user_list);
	user_list.push(user);
	localStorage.setItem("user_list", JSON.stringify(user_list));
}


function validate_password(pass)
{
	let error_msg = null
	let password_regex = new RegExp("^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])");
	
	if((pass.length <= 5) || (pass.length > 20))
		error_msg = "Passwords length must be between 5 and 20";			
	else if(!password_regex.test(pass))
		error_msg = "Invalid Password";			
	else
		return true
	document.getElementById('password_error').innerHTML = " ** " + error_msg;
	return false;	
}


function validate_confirmPaasword(pass, confirm_pass)
{
	let error_msg = null
	if(pass != confirm_pass)
		error_msg = "Password does not match the confirm password";
	else
		return true
	document.getElementById('confirmPassword_error').innerHTML = " ** " + error_msg;	
	return false;
}


function validate_mobileNumber(mobileNumber)
{
	let error_msg = null
	if(isNaN(mobileNumber))
		error_msg =" ** user must write digits only not characters";
	else if(mobileNumber.length!=11)
		error_msg = " ** Mobile Number must be 10 digits only";
	else 
		return true
	document.getElementById('mobileNumber_error').innerHTML = " ** " + error_msg;	
	return false

}


function clear_fields()
{
	document.getElementById('username').value = "";
	document.getElementById('password').value = "";
	document.getElementById('confirmPassword').value = "";
	document.getElementById('mobileNumber').value = "";
	document.getElementById('email').value = "";
}


function clear_errors()
{
	document.getElementById('username_error').innerHTML = "";
	document.getElementById('password_error').innerHTML = "";
	document.getElementById('confirmPassword_error').innerHTML = "";
	document.getElementById('mobileNumber_error').innerHTML = "";
}


function clear_all()
{
	clear_fields();
	clear_errors();
}


function validation(event)
{
	let user = document.getElementById('username').value;
	let pass = document.getElementById('password').value;
	let confirm_pass = document.getElementById('confirmPassword').value;
	let mobileNumber = document.getElementById('mobileNumber').value;
	let email = document.getElementById('email').value;


	fetch(`http://localhost:3000/users?username=${user}`)
	.then(response => response.json())
	.then(user_data => 
	{
		if(user_data.length)
		{
			document.getElementById('username_error').innerHTML = " **Already registered, try another";
			return false
		}
		if(validate_password(pass) && validate_confirmPaasword(pass, confirm_pass) && validate_mobileNumber(mobileNumber))
		{
			let formData = {
				"username": user,
				"email": email,
				"password": pass,
				"mobileNumber": mobileNumber
			};

			$.ajax(
			{
				type        : 'POST',
				url         : 'http://localhost:3000/users', 
				data        : formData, 
				dataType    : 'json' 
			})
			.done(function(data) {
				clear_all()
				alert("successfully registered")				
			})
		}
	}).catch(alert);
	
	return false
}