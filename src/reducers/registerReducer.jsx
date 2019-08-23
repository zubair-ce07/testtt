import { REGISTER_ERROR, REGISTER_SUCCESS } from "../actions/actions.types";

const INITIAL_STATE = {
  status: "",
  message: ""
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case REGISTER_SUCCESS:
      return action.payload;
    case REGISTER_ERROR:
      return action.payload;
    default:
      return state;
  }
};
