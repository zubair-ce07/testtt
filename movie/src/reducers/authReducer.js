import { types } from "../actions/types";

const initailState = {
  loading: false,
  user: {
    email: "",
    first_name: "",
    last_name: "",
    gender: "",
    date_of_birth:  "",
    password: "",
    confirm_password: ""
  },
  isAuthenticated: false,
  error: null,
  isLoginForm: true
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
        isAuthenticated: true
      };
    case types.AUTH_USER_FAILURE:
      return {
        ...state,
        loading: false,
        error: action.payload.error,
        isAuthenticated: false
      };
    default:
      return state;
  }
};

export default authReducer;
