import API from '../api/api';
import * as types from './actionTypes.js';

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
            let api = new API();
            api.user(state.login_reducer.token).then(json => dispatch(receiveUser(json)));
    }
    else
    {
      return dispatch(receiveUser({username : ""}));
    }
  };
}