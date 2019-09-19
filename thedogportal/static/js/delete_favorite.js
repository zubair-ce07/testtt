const FAV_DELETE_BTN = document.getElementsByClassName("fav-delete-button")
const QUERY = `${BASE_URL}/api/portal/delete_favorite/`

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

Array.from(FAV_DELETE_BTN).forEach((ele) => {
    ele.addEventListener('click', (e) => {
        let imageId = e.currentTarget.value
        let params = `favorite=${imageId}`;
        let csrftoken = getCookie('csrftoken')
        portalAPICaller(QUERY, params, csrftoken)
        .then((returnedJsonData) => {
            document.getElementById(`fav-${imageId}`).remove()
        })
        .catch((e) => {
            console.log(e);
        })
        e.preventDefault();
    })
})


function portalAPICaller(QUERY, params, csrftoken) {
    return new Promise(function(resolve, reject) {
        let clientRequest = new XMLHttpRequest();
        clientRequest.open(REQ_METHOD, QUERY, ASYNC_API_CALL);
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