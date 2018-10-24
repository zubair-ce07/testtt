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
    errorMsg = PASSWORD_ERROR.length;
  }
  else if(!passwordRegex.test(pass))
  {
    errorMsg = PASSWORD_ERROR.regex;
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
    errorMsg = PASSWORD_ERROR.misMatched;
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
    errorMsg = MOBILE_ERROR.notDigit;
  }
  else if(mobileNumber.length!=11)
  {
    errorMsg = MOBILE_ERROR.length;
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
 * reason: return object after getting values from all fields
*/
function getFieldsData()
{
  fieldsData = {}
  fieldsData.username = getValue(`username`);
  fieldsData.password = getValue(`password`);
  fieldsData.confirmPass = getValue(`confirmPassword`);
  fieldsData.mobileNumber = getValue(`mobileNumber`);
  fieldsData.email = getValue(`email`);
  return fieldsData
}


/**
 * reason: register user through API call
*/
function registerUser(formData)
{

  makeAjaxCall(`POST`, `${BASEURL}/users`, formData)
    .done(function() {
      clearAll();
      alert(SUCESSFULLY_REGISTERED_MSG);
    });
}


/**
 * reason: needed to validate username after making API call
 *   username should be unique
*/
function validateUsername(username)
{
  return getUserList(username)
    .then(userData =>
    {
      if(userData.length)
      {
        displayNameError(USERNAME_ERROR);
        return false;
      }
      else
      {
        return true
      }
    })
}


/**
 * reason: calls when user clik on sign up button
 *   + do all the validations after getting user list through API call
*/
function validation()
{
  clearErrors();
  let fieldsData = getFieldsData();
  validateUsername(fieldsData.username)
    .then(isValidUsername => 
    {
      if(isValidUsername &&
         validatePassword(fieldsData.password) &&
         validateMobileNumber(fieldsData.mobileNumber) &&
         validateConfirmPaasword(fieldsData.password, fieldsData.confirmPass))
      {
        delete fieldsData.confirmPass
        registerUser(fieldsData)
      }
    })
    .catch(console.err)
  return false;
}
