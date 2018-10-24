function displayLoginError()
{
  document.getElementById(`loginError`).innerHTML = ` ** ${LOGIN_ERROR}`;
}


function loginUser(userList, password)
{
  if(userList.length && userList[0].password == password)
  {
    localStorage.setItem(`loggedInUser`, JSON.stringify(userList[0]));
    window.location.replace(`home.html`);
  }
  else
  {
    displayLoginError()
  } 
}


function authenticate()
{
  document.getElementById(`loginError`).innerHTML = '';
  let username = document.getElementById(`loginUsername`).value;
  let password = document.getElementById(`loginPassword`).value;

  getUserList(username)
    .then(userList => loginUser(userList, password))
    .catch(console.error);
  return false;
}
