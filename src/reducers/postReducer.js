import _ from "lodash";
import {
  CREATE_POST,
  FETCH_FEED,
  DELETE_POST,
  FETCH_USER_POSTS,
  LOGOUT
} from "../actions/actions.types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case CREATE_POST: {
      return { ...state, [action.payload.id]: action.payload };
    }
    case FETCH_FEED: {
      return { ...state, ..._.mapKeys(action.payload, "id") };
    }
    case DELETE_POST: {
      const newState = { ...state };
      delete newState[action.payload];
      return { ...newState };
    }
    case FETCH_USER_POSTS: {
      return { ..._.mapKeys(action.payload, "id") };
    }
    case LOGOUT:
      return INITIAL_STATE;
    default:
      return state;
  }
};
