import * as types from './actionTypes';

function url() {
  return 'http://127.0.0.1:8000/auth';
}

export function receiveToken(json) {
  return {type: types.RECEIVE_TOKEN, receivedToken: json.token};
}

export function logout() {
  return (dispatch)=>(dispatch({type: types.CLOSE_SESSION}));
}


export function requestAuthorization(credentials) {
	var payload = { username: credentials.name,
                  password: credentials.password }
  return (dispatch) => {
    return fetch(url(), {
      method: 'POST',
      mode: 'cors',
      headers: {
        "Content-Type": "application/json;charset=UTF-8"
      },
      body:JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(json => dispatch(receiveToken(json)));
  };
}