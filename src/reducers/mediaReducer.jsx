import { ADD_MEDIA, REMOVE_MEDIA, CLEAR_MEDIA } from "../actions/actions.types";

const INITIAL_STATE = [];

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case ADD_MEDIA:
      return [...state, action.payload];
    case REMOVE_MEDIA:
      return state.filter(media => media !== action.payload);
    case CLEAR_MEDIA:
      return INITIAL_STATE;
    default:
      return state;
  }
};
