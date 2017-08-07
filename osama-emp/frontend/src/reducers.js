import { GET_PROFILE_END } from "./actions";

const initialState = {
  profile: {},
  hierarchy: {}
};

function rootReducer(state = initialState, action) {
  switch (action.type) {
    case GET_PROFILE_END:
      return Object.assign({}, state, {
        profile: action.profile
      });
    default:
      return state;
  }
}

export default rootReducer;
