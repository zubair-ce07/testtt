import { SEARCH_YOUTUBE, END_REQUEST } from "./actions";

const initialState = {
  results: []
};

const search = (state = initialState, action) => {
  switch (action.type) {
    case SEARCH_YOUTUBE:
      return state;
    case END_REQUEST:
      return Object.assign({}, state, {
        results: action.results
      });
    default:
      return state;
  }
};

const rootReducer = search;

export default rootReducer;
