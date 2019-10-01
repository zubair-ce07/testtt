import { types } from "../actions/types";

const initialState = {
  isLoginForm: true
};

const formReducer = (state = initialState, action) => {
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
