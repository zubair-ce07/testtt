import {
  LOADING_BLOG_DETAIL,
  UPDATE_BLOG_DETAIL,
  RESET_BLOG_DETAIL,
  BLOG_DETAIL_ERRORS,
  BLOG_DETAIL_LOADED,
} from './actions';

const INITIAL_STATE = {
  loading: false,
  loaded: false,
  blog: {
    id: 0,
    title: '',
    body: '',
    tags: [],
  },
  errors: [],
};

export const BlogDetailReducer = (state = { ...INITIAL_STATE }, action) => {
  switch (action.type) {
    case LOADING_BLOG_DETAIL:
      return { ...state, loading: true };

    case BLOG_DETAIL_LOADED:
      return { ...state, loading: false, loaded: true };

    case RESET_BLOG_DETAIL:
      return { ...INITIAL_STATE };

    case UPDATE_BLOG_DETAIL:
      return {
        ...state,
        blog: { ...state.blog, ...action.payload }
      };

    case BLOG_DETAIL_ERRORS:
      return { ...state, errors: action.payload };

    default:
      return state;
  }
};
