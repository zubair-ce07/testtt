import * as types from './actionTypes.js';

function url() {
  return 'http://127.0.0.1:8000/current_user';
}

export function receiveUser(json) {
  if(typeof json.username !== "undefined")
  {
    return {type: types.RECEIVE_USER, user: json.username};
  }
  else
  {
    return {type: types.DEFAULT};
  }
}

export function fetchUser() {
  return (dispatch, getState) => {
    var state = getState();
    if(state.login_reducer.token !== "")
    {
      return fetch(url(), {
        method: 'GET',
        mode: 'cors',
        headers: {
          "Authorization" : "Token "+state.login_reducer.token
        },
      }).then(response => response.json())
        .then(json => dispatch(receiveUser(json)));
    }
    else
    {
      return dispatch(receiveUser({username : ""}));
    }
  };
}