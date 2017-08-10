export function login(username, password, callback) {
  const loginData = {
    username,
    password
  };
  const headers = {
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
  const headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: 'Token ' + localStorage.token

  };

  const request = new Request(URL, {
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

export function createOrUpdateBrand(formData, is_update, callback ){
  const headers = {
    Accept: "application/json",
    Authorization: 'Token ' + localStorage.token,
  };

  const data = new FormData()
  data.append('pk', parseInt(formData.pk.value.toString(), 10))
  data.append('name', formData.name.value.toString())
  data.append('brand_link', formData.brand_link.value.toString())
  if (formData.image_icon.files.length > 0){
    data.append('image_icon', formData.image_icon.files[0])
  }
  let URL = ''
  let method = 'post'

  if(is_update){
    URL = 'http://localhost:8000/api/brand/'+formData.pk.value.toString()+'/'
    method = 'PATCH'
  }else{
    URL = 'http://localhost:8000/api/brand/create/'
    method='post'
  }

  fetch(URL, {
    method,
    headers,
    mode: "cors",
    redirect: "follow",
    body: data
  }).then(response => response.json()).then(callback).catch(response => console.log(response));
}


export function getOrDeleteBrand(pk, method, callback){
  let headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
    Authorization: 'Token ' + localStorage.token,
  };
  console.log(method)
  fetch('http://localhost:8000/api/brand/'+pk, {
    method,
    headers,
    mode: "cors",
    redirect: "follow",
  }).then(response => response.json()).then(callback);
}
