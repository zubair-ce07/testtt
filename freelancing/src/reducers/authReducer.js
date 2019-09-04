import { LOGGING_USER, LOGIN_SUCESS, LOGIN_FAILED } from "../actions/types";

const initialState = {
  token: null,
  uid: null,
  authErrors: [],
  isLogging: false
};
export const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGIN_SUCESS:
      console.log("login success", action.payload);
      return {
        ...state,
        token: action.payload,
        isLogging: false,
        authErrors: []
      };

    case LOGIN_FAILED:
      console.log("login failed", action.payload);
      const prevErrors = state.authErrors;
      prevErrors.push(action.payload);
      return {
        ...state,
        authErrors: prevErrors,
        isLogging: false
      };

    case LOGGING_USER:
      console.log("logging user");
      return {
        ...state,
        authErrors: [],
        isLogging: true
      };

    default:
      return state;
  }
};
