import { types } from "../actions/types";

const initailState = {
  user: {}
};

const userReducer = (state = initailState, action) => {
  switch (action.type) {
    case types.UPDATE_USER:
      return {
        ...state,
        user: action.payload.user
      };
    default:
      return state;
  }
};

export default userReducer;
