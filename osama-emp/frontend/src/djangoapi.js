import { loggedIn } from "./auth";
import { SERVER_URL } from "./constants";

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
  let request = new Request(SERVER_URL + "obtain-auth-token/", {
    method: "post",
    headers,
    mode: "cors",
    redirect: "follow",
    body: JSON.stringify(loginData)
  });

  fetch(request)
    .then(response => response.json())
    .then(callback)
    .catch(error => console.log(error));
}

function getProfile(username, callback) {
  fetch(SERVER_URL + "employees/" + username + "/", {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback)
    .catch(error => console.log(error));
}

function getDirects(username, callback) {
  fetch(SERVER_URL + "employees/" + username + "/directs", {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback)
    .catch(error => console.log(error));
}

function listEmployees(callback) {
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: "Token " + localStorage.token
  };
  fetch(SERVER_URL + "employees/", {
    method: "get",
    headers
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback)
    .catch(error => console.log(error));
}

let djangoapi = {
  login,
  getProfile,
  getDirects,
  listEmployees
};

export default djangoapi;
