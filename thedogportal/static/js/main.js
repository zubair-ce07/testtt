const HOME_UP_BTN = document.getElementById("home-up-btn");
const HOME_DWN_BTN = document.getElementById("home-dwn-btn");
const HOME_FAV_BTN = document.getElementById("home-fav-btn");
const HOME_IMG = document.getElementById("home-img");
const HOME_IMG_TITLE = document.getElementById("home-img-title");
const HOME_IMG_UPVOTES = document.getElementById("home-img-upvotes");
const HOME_IMG_DOWNVOTES = document.getElementById("home-img-downvotes");
const HOME_IMG_FAVORITES = document.getElementById("home-img-favorites");
const BTN_NORMAL_CLASS_LIST = "btn waves-effect waves-light"
const BTN_PRESSED_CLASS_LIST = "btn waves-effect waves-light pressed"
const QUERY = `${BASE_URL}/api/portal/post_reaction/`


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

HOME_UP_BTN.addEventListener('click', (e) => {
    let params = `upvote=${e.currentTarget.value}`;
    let csrftoken = getCookie('csrftoken')
    portalAPICaller(QUERY, params, csrftoken)
    .then((returnedJsonData) => {
        render_new_image(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    e.preventDefault();
})


HOME_DWN_BTN.addEventListener('click', (e) => {
    let params = `downvote=${e.currentTarget.value}`;
    let csrftoken = getCookie('csrftoken')
    portalAPICaller(QUERY, params, csrftoken)
    .then((returnedJsonData) => {
        render_new_image(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    e.preventDefault();
})


HOME_FAV_BTN.addEventListener('click', (e) => {
    let params = `favorite=${e.currentTarget.value}`;
    let csrftoken = getCookie('csrftoken')
    portalAPICaller(QUERY, params, csrftoken)
    .then((returnedJsonData) => {
        render_new_image(returnedJsonData);
    })
    .catch((e) => {
        console.log(e);
    })
    e.preventDefault();
})


function render_new_image(data) {
    HOME_IMG_TITLE.innerText = data.title
    HOME_IMG.src = data.url
    HOME_IMG_UPVOTES.innerText = data.upvotes
    HOME_IMG_DOWNVOTES.innerText = data.downvotes
    HOME_IMG_FAVORITES.innerText = data.favorites
    HOME_UP_BTN.value = data.pk
    HOME_DWN_BTN.value = data.pk
    HOME_FAV_BTN.value = data.pk

    if(data.upvoted) {
        HOME_UP_BTN.classList = BTN_PRESSED_CLASS_LIST
    } else {
        HOME_UP_BTN.classList = BTN_NORMAL_CLASS_LIST
    }

    if(data.downvoted) {
        HOME_DWN_BTN.classList = BTN_PRESSED_CLASS_LIST
    } else {
        HOME_DWN_BTN.classList = BTN_NORMAL_CLASS_LIST
    }

    if(data.favorited) {
        HOME_FAV_BTN.classList = BTN_PRESSED_CLASS_LIST
    } else {
        HOME_FAV_BTN.classList = BTN_NORMAL_CLASS_LIST
    }
}


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
