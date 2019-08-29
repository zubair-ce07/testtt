import { LOGIN_ERROR, LOGIN_SUCCESS, LOGOUT } from "../actions/actions.types";

const INITIAL_STATE = {
  isSignedIn: false
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOGIN_ERROR:
      return action.payload;
    case LOGIN_SUCCESS:
      const { user_id, access } = action.payload;
      return { isSignedIn: true, user_id: user_id, access: access };
    case LOGOUT:
      return INITIAL_STATE;
    default:
      return state;
  }
};
