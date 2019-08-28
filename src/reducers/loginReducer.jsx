import { LOGIN_ERROR, LOGIN_SUCCESS, LOGOUT } from "../actions/actions.types";

const INITIAL_STATE = {
  isSignedIn: false
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOGIN_ERROR:
      return action.payload;
    case LOGIN_SUCCESS:
      return { isSignedIn: true, user_id: action.payload };
    case LOGOUT:
      return INITIAL_STATE;
    default:
      return state;
  }
};
