import { types } from "../actions/types";

const initailState = {
  isLoginForm: true
};

const formReducer = (state = initailState, action) => {
  switch (action.type) {
    case types.LOGIN_FORM:
      return {
        ...state,
        isLoginForm: !state.isLoginForm
      };
    default:
      return state;
  }
};

export default formReducer;
