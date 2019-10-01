import { types } from "../actions/types";

const initailState = {
  loading: false,
  user: {},
  isAuthenticated: false,
  error: null
};

const authReducer = (state = initailState, action) => {
  switch (action.type) {
    case types.AUTH_USER_STARTED:
      return {
        ...state,
        loading: true
      };
    case types.AUTH_USER_SUCCESS:
      return {
        ...state,
        loading: false,
        user: action.payload.user,
        isAuthenticated: true,
        error: null
      };
    case types.AUTH_USER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error,
        isAuthenticated: false,
        user: {}
      };
    case types.LOGOUT_USER:
      return {
        ...state,
        isAuthenticated: false,
        user: {},
        error: false
      };
    default:
      return state;
  }
};

export default authReducer;
