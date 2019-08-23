import _ from "lodash";
import { FETCH_USER, FETCH_ALL_USERS } from "../actions/actions.types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_USER:
      return { ...state, [action.payload.id]: action.payload };
    case FETCH_ALL_USERS:
      return { ...state, ..._.mapKeys(action.payload, "id") };
    default:
      return state;
  }
};
