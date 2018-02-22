import API from '../../api/api';
import * as types from './actionTypes.js';

export function receiveFreelancers(json) {
    return {type: types.RECEIVE_FREELANCERS, freelancers: json};
}

export function fetchFreelancers() {
  return (dispatch, getState) => {
    var state = getState();
    if(state.login_reducer.token !== "")
      { 
        let api = new API();
        return api.freelancers(state.login_reducer.token)
            .then(json => dispatch(receiveFreelancers(json)));
    }
    else
    {
      return dispatch(receiveFreelancers({freelancers : []}));
    }
  };
}
