import { LOGGING_USER, LOGIN_SUCESS } from "../actions/types";

const initialState = {
  token: null,
  uid: null,
  isLogging: false
};
export const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case LOGGING_USER:
      console.log("logging user in");
      return {
        ...state,
        isLogging: true
      };
    case LOGIN_SUCESS:
      console.log("login success");
      return {
        ...state,
        isLogging: false
      };
    default:
      return state;
  }
};
