import { combineReducers } from "redux";

import { SEARCH_YOUTUBE } from "./actions";

const search = (state = [], action) => {
  switch (action.type) {
    case SEARCH_YOUTUBE:
      console.log("hello");
      return state.concat("hello");
    default:
      return state;
  }
};

// const rootReducer = combineReducers({
//   search
// });

const rootReducer = search;

export default rootReducer;
