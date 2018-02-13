import * as types from './actionTypes.js';

function url() {
  return 'http://127.0.0.1:8000/freelancers';
}

export function receiveFreelancers(json) {
    return {type: types.RECEIVE_FREELANCERS, freelancers: json};
}

export function fetchFreelancers() {
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
        .then(json => dispatch(receiveFreelancers(json)));
    }
    else
    {
      return dispatch(receiveFreelancers({freelancers : []}));
    }
  };
}