import { types } from "../actions/types";

const initialState = {
  form: {}
};

const formReducer = (state = initialState, action) => {
  switch (action.type) {
    case types.UPDATE_FORM:
      return {
        ...state,
        form: action.payload.form
      };
    default:
      return state;
  }
};

export default formReducer;
