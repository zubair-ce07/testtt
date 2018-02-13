import initialState from './initialState.js';
import {FETCH_USER, RECEIVE_USER} from './actionTypes.js';

export default function reducer(state = initialState, action) {
  let newState;
  switch (action.type) {
    case FETCH_USER:
      console.log('FETCH_USER Action')
      return action;
    case RECEIVE_USER:
      newState = {
        user: action.user
      }
      console.log('RECEIVE_USER Action')
      return newState;
    default:
      return state;
  }
}