/**
 * reason: if no logged in user, redirect him to index page.
*/
if(!localStorage.getItem(`loggedin_user`)) {
  window.location.href = `index.html`;
}
