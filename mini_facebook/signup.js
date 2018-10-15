function displayPasswordError(errorMsg) {
  document.getElementById(`passwordError`).innerHTML = ` ** ${errorMsg}`;
}


function displayConfirmPasswordError(errorMsg) {
  document.getElementById(`confirmPasswordError`).innerHTML = ` ** ${errorMsg}`;
}


function displayNumberError(errorMsg) {
  document.getElementById(`mobileNumberError`).innerHTML = ` ** ${errorMsg}`;
}


function displayNameError(errorMsg)
{
  document.getElementById(`usernameError`).innerHTML = ` ** ${errorMsg}`;
}


function validatePassword(pass)
{
  let errorMsg = null;
  let passwordRegex = new RegExp(`^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])`);
  if((pass.length <= 5) || (pass.length > 20))
  {
    errorMsg = `Passwords length must be between 5 and 20`;
  }
  else if(!passwordRegex.test(pass))
  {
    errorMsg = `Invalid Password`;
  }
  else
  {
    return true;
  }
  displayPasswordError(errorMsg);
  return false;
}


function validateConfirmPaasword(pass, confirmPass)
{
  let errorMsg = null;
  if(pass != confirmPass)
  {
    errorMsg = `Password does not match the confirm password`;
  }
  else
  {
    return true;
  }
  displayConfirmPasswordError(errorMsg);
  return false;
}


function validateMobileNumber(mobileNumber)
{
  let errorMsg = null;
  if(isNaN(mobileNumber))
  {
    errorMsg =`Characters are not allowed`;
  }
  else if(mobileNumber.length!=11)
  {
    errorMsg = `Mobile Number must be 10 digits only`;
  }
  else
  {
    return true;
  }
  displayNumberError(errorMsg);
  return false;
}


function clearFields()
{
  document.getElementById(`username`).value = ``;
  document.getElementById(`password`).value = ``;
  document.getElementById(`confirmPassword`).value = ``;
  document.getElementById(`mobileNumber`).value = ``;
  document.getElementById(`email`).value = ``;
}


function clearErrors()
{
  document.getElementById(`usernameError`).innerHTML = ``;
  document.getElementById(`passwordError`).innerHTML = ``;
  document.getElementById(`confirmPasswordError`).innerHTML = ``;
  document.getElementById(`mobileNumberError`).innerHTML = ``;
}


function clearAll()
{
  clearFields();
  clearErrors();
}


function validation()
{
  clearErrors();
  let username = document.getElementById(`username`).value;
  let password = document.getElementById(`password`).value;
  let confirmPass = document.getElementById(`confirmPassword`).value;
  let mobileNumber = document.getElementById(`mobileNumber`).value;
  let email = document.getElementById(`email`).value;

  fetch(`${baseUrl}/users?username=${username}`)
    .then(response => response.json())
    .then(userData =>
    {
      if(userData.length)
      {
        displayNameError(`Already registered, try another.`);
        return false;
      }
      if(validatePassword(password) &&
         validateConfirmPaasword(password, confirmPass) &&
         validateMobileNumber(mobileNumber))
      {

        let formData = {
          username,
          email,
          password,
          mobileNumber
        };

        $.ajax({
          type        : `POST`,
          url         : `${baseUrl}/users`,
          data        : formData,
          dataType    : `json`
        })
          .done(function() {
            clearAll();
            alert(`successfully registered`);
          });
      }
    }).catch(console.error);
  return false;
}
