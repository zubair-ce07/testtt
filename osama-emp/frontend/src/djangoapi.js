function login(username, password, callback) {
  let loginData = {
    username,
    password
  };
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json"
  };

  let request = new Request("http://localhost:8000/obtain-auth-token/", {
    method: "post",
    headers,
    mode: "cors",
    redirect: "follow",
    body: JSON.stringify(loginData)
  });

  fetch(request).then(response => response.json()).then(callback);
}

function getProfile(callback) {
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: "Token " + localStorage.token
  };
  fetch("http://localhost:8000/employees/" + localStorage.username, {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback);
}

function listEmployees(callback) {
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: "Token " + localStorage.token
  };
  fetch("http://localhost:8000/employees/", {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback);
}

let djangoapi = {
  login,
  getProfile,
  listEmployees
};

export default djangoapi;
