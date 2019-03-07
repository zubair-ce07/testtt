import {
  LOADING_BLOG, UPDATE_BLOG, RESET_BLOG, BLOG_ERRORS, BLOG_LOADED
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  blog: {
    title: '',
    body: '',
    tags: [],
  },
  errors: [],
};

export const CreateBlogReducer = (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case LOADING_BLOG:
      return { ...state, loading: true };

    case BLOG_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_BLOG:
      return INITIAL_STATE;

    case UPDATE_BLOG:
      return {
        ...state,
        blog: { ...state.blog, ...action.payload }
      };

    case BLOG_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
