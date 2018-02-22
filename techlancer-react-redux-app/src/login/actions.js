import API from '../api/api';
import * as types from './actionTypes';

export function receiveToken(json) {
  return {type: types.RECEIVE_TOKEN, receivedToken: json.token};
}

export function logout() {
  return (dispatch)=>(dispatch({type: types.CLOSE_SESSION}));
}

export function requestAuthorization(credentials) {
    let  api = new API();
    return (dispatch) => {
        api.authorize(credentials).then(json => dispatch(receiveToken(json)));
    }
}

