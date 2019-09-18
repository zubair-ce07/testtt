const FAV_DELETE_BTN = document.getElementById("fav-delete-button")
const REQ_METHOD = 'POST'
const RES_TYPE = 'json'
const ASYNC_API_CALL = true;
const API_REQUEST_SUCCESSFUL = 200;
const REQUEST_FAILED_MESSAGE = "Failed 200 OK => API Request was not successful!";


let base_url = window.location.origin


function getCookie(name) {
    if (!document.cookie) {
      return null;
    }
  
    const xsrfCookies = document.cookie.split(';')
      .map(c => c.trim())
      .filter(c => c.startsWith(name + '='));
  
    if (xsrfCookies.length === 0) {
      return null;
    }
  
    return decodeURIComponent(xsrfCookies[0].split('=')[1]);
}

FAV_DELETE_BTN.addEventListener('click', (e) => {
    console.log("was called, event listener")
    let imageId = e.currentTarget.value
    console.log("Delete ", imageId)
    let query = `${base_url}/api/portal/delete_favorite/`
    let params = `favorite=${imageId}`;
    let csrftoken = getCookie('csrftoken')
    portalAPICaller(query, params, csrftoken)
    .then((returnedJsonData) => {
        console.log(`fav-${imageId}`)
        document.getElementById(`fav-${imageId}`).remove()
    })
    .catch((e) => {
        console.log(e);
    })
    e.preventDefault();
})


function portalAPICaller(query, params, csrftoken) {
    return new Promise(function(resolve, reject) {
        let clientRequest = new XMLHttpRequest();
        clientRequest.open(REQ_METHOD, query, ASYNC_API_CALL);
        clientRequest.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        clientRequest.setRequestHeader("X-CSRFToken", csrftoken);
        clientRequest.responseType = RES_TYPE;
        clientRequest.onload = function() {
            if (clientRequest.status == API_REQUEST_SUCCESSFUL) {
                resolve(clientRequest.response);
            } else {
                reject(new Error(REQUEST_FAILED_MESSAGE));
            }
        }
        clientRequest.send(params);
    })
}