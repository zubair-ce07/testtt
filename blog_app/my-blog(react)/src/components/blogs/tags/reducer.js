import {
  LOADING_TAGS, UPDATE_TAGS, RESET_TAGS, TAGS_LOADED, TAGS_ERRORS
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  tags: [],
  errors: [],
};

export const TagsReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOADING_TAGS:
      return { ...state, loading: true };

    case TAGS_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_TAGS:
      return INITIAL_STATE;

    case UPDATE_TAGS:
      return { ...state, tags: action.payload };

    case TAGS_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
