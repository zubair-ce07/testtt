import {combineReducers} from 'redux';

import initialState from './initialState.js';
import login_reducer from './login/reducers.js';
import nav_reducer from './nav/reducer.jsx';
import freelancer_reducer from './freelancer/listing/reducer';


function app_reducer(state = initialState, action) {
  switch (action.type) {
    default:
      return state;
  }
}

const rootReducer = combineReducers({
  freelancer_reducer,
  app_reducer,
  nav_reducer,
  login_reducer
});

export default rootReducer;