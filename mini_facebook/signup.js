/**
 * reason: needed to display Password error msgs
*/
function displayPasswordError(errorMsg) {
  document.getElementById(`passwordError`).innerHTML = ` ** ${errorMsg}`;
}


/**
 * reason: needed to display Confirm password error msgs
*/
function displayConfirmPasswordError(errorMsg) {
  document.getElementById(`confirmPasswordError`).innerHTML = ` ** ${errorMsg}`;
}


/**
 * reason: needed to display mobile Number error msgs
*/
function displayNumberError(errorMsg) {
  document.getElementById(`mobileNumberError`).innerHTML = ` ** ${errorMsg}`;
}


/**
 * reason: needed to display usrename error msg
*/
function displayNameError(errorMsg)
{
  document.getElementById(`usernameError`).innerHTML = ` ** ${errorMsg}`;
}


/**
 * reason: needed to validate password 
 *   password length must in range(5 to 20)
 *   password must contain atleast
 *     1 uppercase, 1 lowercase & 1 special character (!@#$%^&*)
*/
function validatePassword(pass)
{
  let errorMsg = null;
  let passwordRegex = new RegExp(`^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#\$%\^&\*])`);
  if((pass.length <= 5) || (pass.length > 20))
  {
    errorMsg = passwordError.length;
  }
  else if(!passwordRegex.test(pass))
  {
    errorMsg = passwordError.regex;
  }
  else
  {
    return true;
  }
  displayPasswordError(errorMsg);
  return false;
}


/**
 * reason: needed to validate confirm password 
 *   password and confirmPassword must be matched
*/
function validateConfirmPaasword(pass, confirmPass)
{
  let errorMsg = null;
  if(pass != confirmPass)
  {
    errorMsg = passwordError.misMatched;
  }
  else
  {
    return true;
  }
  displayConfirmPasswordError(errorMsg);
  return false;
}


/**
 * reason: needed to validate mobile Number
 *   mobile number should only contain disgits and must be of length 11
*/
function validateMobileNumber(mobileNumber)
{
  let errorMsg = null;
  if(isNaN(mobileNumber))
  {
    errorMsg = mobileError.notDigit;
  }
  else if(mobileNumber.length!=11)
  {
    errorMsg = mobileError.length;
  }
  else
  {
    return true;
  }
  displayNumberError(errorMsg);
  return false;
}


/**
 * reason: needed clear field on the base of id
*/
function clearField(id)
{
  document.getElementById(id).value = '';
}


/**
 * reason: needed clear error msg on the base of id
*/
function clearMsg(id)
{
  document.getElementById(id).innerHTML = '';
}


/**
 * reason: needed clear all fields
*/
function clearAllFields()
{
  clearField(`username`);
  clearField(`password`);
  clearField(`confirmPassword`);
  clearField(`mobileNumber`);
  clearField(`email`);
}


/**
 * reason: needed clear all error msgs
*/
function clearErrors()
{
  clearMsg(`usernameError`);
  clearMsg(`passwordError`);
  clearMsg(`confirmPasswordError`);
  clearMsg(`mobileNumberError`);
}


/**
 * reason: needed clear all fields and all error msgs
*/
function clearAll()
{
  clearAllFields();
  clearErrors();
}


/**
 * reason: needed to get value from specific field on the bases of give id
*/
function getValue(id)
{
  return document.getElementById(id).value;
}


/**
 * reason: calls when user clik on sign up button
 *   + done all the validations after getting user list through API call
*/
function validation()
{
  clearErrors();
  let username = getValue(`username`);
  let password = getValue(`password`);
  let confirmPass = getValue(`confirmPassword`);
  let mobileNumber = getValue(`mobileNumber`);
  let email = getValue(`email`);

  fetch(`${BASEURL}/users?username=${username}`)
    .then(response => response.json())
    .then(userData =>
    {
      if(userData.length)
      {
        displayNameError(usernameError);
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
          url         : `${BASEURL}/users`,
          data        : formData,
          dataType    : `json`
        })
          .done(function() {
            clearAll();
            alert(registerSuccessMsg);
          });
      }
    }).catch(console.error);
  return false;
}
