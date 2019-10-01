import { types } from "../actions/types";

const initialState = {
  user: {
    
  }
};

const userReducer = (state = initialState, action) => {
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
