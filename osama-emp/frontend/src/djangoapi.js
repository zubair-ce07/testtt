function login(callback) {
  fetch("http://localhost:8000/employees/");
}

function listEmployees(callback) {
  fetch("http://localhost:8000/employees/", {
    method: "get"
  })
    .then(function(response) {
      return response.json();
    })
    .then(callback);
}

let djangoapi = {
  login,
  listEmployees
};

export default djangoapi;
