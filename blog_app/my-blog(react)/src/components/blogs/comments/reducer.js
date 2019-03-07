import {
  LOADING_COMMENTS,
  UPDATE_COMMENTS,
  RESET_COMMENTS,
  COMMENTS_ERRORS,
  COMMENTS_LOADED,
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  comments: [],
  errors: [],
};

export const CommentsReducer = (state = { ...INITIAL_STATE }, action) => {
  switch (action.type) {
    case LOADING_COMMENTS:
      return { ...state, loading: true };

    case COMMENTS_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_COMMENTS:
      return { ...INITIAL_STATE };

    case UPDATE_COMMENTS:
      return {
        ...state,
        comments: action.payload
      };

    case COMMENTS_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
