export function login(username, password, callback) {
  let loginData = {
    username,
    password
  };
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json"
  };

  let request = new Request("http://localhost:8000/api/api-login/", {
    method: "post",
    headers,
    mode: "cors",
    redirect: "follow",
    body: JSON.stringify(loginData)
  });

  fetch(request).then(response => response.json()).then(callback);
}


export function listItems(URL, callback){
    let headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: 'Token ' + localStorage.token

  };

  let request = new Request(URL, {
    method: "get",
    headers,
    mode: "cors",
    redirect: "follow",
  });

  fetch(request).then(response => response.json()).then(callback);
}


export function logout () {
    delete localStorage.token

}

export function loggedIn () {
    return !!localStorage.token
}

