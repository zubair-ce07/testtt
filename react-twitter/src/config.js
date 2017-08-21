let domain = "http://127.0.0.1:8000/api";
let userToken = localStorage.user ? JSON.parse(localStorage.user).token : null;
export {domain,userToken};