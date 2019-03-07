import {
  LOADING_BLOGS, UPDATE_BLOGS, RESET_BLOGS, BLOGS_ERRORS, BLOGS_LOADED
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  blogs: [],
  errors: [],
};

export const BlogsListReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOADING_BLOGS:
      return { ...state, loading: true };

    case BLOGS_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_BLOGS:
      return INITIAL_STATE;

    case UPDATE_BLOGS:
      return { ...state, blogs: action.payload };

    case BLOGS_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
