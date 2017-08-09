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
    localStorage.removeItem('token')

}

export function loggedIn () {
    return !!localStorage.token
}

export function createBrand(formData, callback ){
    let headers = {
    Accept: "application/json",
    Authorization: 'Token ' + localStorage.token,
  };

  var data = new FormData()
  data.append('name', formData.name.value.toString())
  data.append('brand_link', formData.brand_link.value.toString())
  data.append('image_icon', formData.image_icon.files[0])

  // let request = new Request('http://localhost:8000/api/brand/create/', {
  //   method: "post",
  //   headers,
  //   mode: "cors",
  //   redirect: "follow",
  //   body: data
  // });

  fetch('http://localhost:8000/api/brand/create/', {
    method: "post",
    headers,
    mode: "cors",
    redirect: "follow",
    body: data
  }).then(response => response.json()).then(callback);
}
