import { FETCH_USER_SUCCESS, LOGOUT_USER } from "../actions/types";

const initialState = {
  data: null
};

export const userReducer = (state = initialState, action) => {
  switch (action.type) {
    case FETCH_USER_SUCCESS:
      console.log("user reducer", action.payload);
      return {
        ...state,
        data: action.payload
      };
    case LOGOUT_USER:
      console.log("logout user");
      return {
        ...state,
        data: null
      };

    default:
      return state;
  }
};
