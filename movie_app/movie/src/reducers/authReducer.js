import { types } from "../actions/types";

const initialState = {
  loading: false,
  user: {},
  isAuthenticated: false,
  error: null
};

const authReducer = (state = initialState, action) => {
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
      };
    case types.LOGOUT_USER:
      return {
        ...state,
        isAuthenticated: false
      };
    default:
      return state;
  }
};

export default authReducer;
