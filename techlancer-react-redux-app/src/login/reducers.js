import initialState from './initialState.js';
import {
REQUEST_AUTHORIZATION,
RECEIVE_TOKEN, CLOSE_SESSION} from './actionTypes.js';

export default function reducer(state = initialState, action) {
  let newState;
  switch (action.type) {
    case REQUEST_AUTHORIZATION:
      console.log('REQUEST_AUTHORIZATION Action')
      return action;
    case RECEIVE_TOKEN:
      newState = { token: action.receivedToken}
      console.log('RECEIVE_TOKEN Action')
      return newState;
    case CLOSE_SESSION:
      newState = { token: ""}
      console.log('CLOSE_SESSION Action')
      return newState;
    default:
      return state;
  }
}