import { types } from "../actions/types";

const initailState = {
  loading: false,
  user: null,
  error: null
};

const loginReducer = (state = initailState, action) => {
  switch (action.type) {
    case types.LOGIN_USER_STARTED:
      return {
        ...state,
        loading: true
      };
    case types.LOGIN_USER_SUCCESS:
      return {
        ...state,
        loading: false,
        error: null,
        user: action.payload
      };
    case types.LOGIN_USER_fAILURE:
      return {
        ...state,
        loading: false,
        user: false,
        error: action.payload
      };
    default:
      return state;
  }
};

export default loginReducer;
