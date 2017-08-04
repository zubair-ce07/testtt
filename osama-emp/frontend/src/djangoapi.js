import { loggedIn } from "./auth";

const headers = {
  Accept: "application/json",
  "Content-Type": "application/json",
  Authorization: loggedIn() ? "Token " + localStorage.token : ""
};

function login(username, password, callback) {
  let loginData = {
    username,
    password
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
  fetch("http://localhost:8000/employees/" + localStorage.username, {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback);
}

function getDirects(username, callback) {
  fetch(
    "http://localhost:8000/employees/" + username + "/directs",
    {
      method: "get",
      headers
    }
  )
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
  getDirects,
  listEmployees
};

export default djangoapi;
