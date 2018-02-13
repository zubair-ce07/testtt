import initialState from './initialState.js';
import {
RECEIVE_FREELANCERS,
FETCH_FREELANCERS} from './actionTypes.js';

export default function reducer(state = initialState, action) {
  let newState;
  switch (action.type) {
    case FETCH_FREELANCERS:
      console.log('FETCH_FREELANCERS Action')
      return action;
    case RECEIVE_FREELANCERS:
      newState = { freelancers: action.freelancers}
      console.log('RECEIVE_FREELANCERS Action')
      return newState;
    default:
      return state;
  }
}