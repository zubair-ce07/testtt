/* exported login */
function authenticate()
{
  document.getElementById(`loginError`).innerHTML = ``;
  let username = document.getElementById(`loginUsername`).value;
  let password = document.getElementById(`loginPassword`).value;

  fetch(`${baseUrl}/users?username=${username}`)
    .then(response => response.json())
    .then(userList =>
    {
      if(userList.length && userList[0].password == password)
      {
        localStorage.setItem(`loggedin_user`, JSON.stringify(userList[0]));
        window.location.replace(`home.html`);
      }
      else
      {
        document.getElementById(`loginError`).innerHTML = ` ** Invalid username or password`;
      }
    })
    .catch(console.error);
  return false;
}
