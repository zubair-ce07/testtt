import Service from '../service';

export const UPDATE_BLOG_DETAIL = 'UPDATE_BLOG_DETAIL';
export const RESET_BLOG_DETAIL = 'RESET_BLOG_DETAIL';
export const LOADING_BLOG_DETAIL = 'LOADING_BLOG_DETAIL';
export const BLOG_DETAIL_LOADED = 'BLOG_DETAIL_LOADED';
export const BLOG_DETAIL_ERRORS = 'BLOG_DETAIL_ERRORS';

const service = new Service();

const reset = () => ({
  type: RESET_BLOG_DETAIL
});

const loading = () => ({
  type: LOADING_BLOG_DETAIL
});

const loaded = () => ({
  type: BLOG_DETAIL_LOADED
});

const update = (fields) => ({
  type: UPDATE_BLOG_DETAIL,
  payload: fields
});

const failed = (errors) => ({
  type: BLOG_DETAIL_ERRORS,
  payload: errors
});

export const load = blogId => async (dispatch) => {
  dispatch(reset());
  dispatch(loading());
  const response = await service.getById(blogId);
  dispatch(loaded());

  if (response.success) {
    dispatch(update(response.data));
  } else {
    dispatch(failed(response.data));
  }
};
