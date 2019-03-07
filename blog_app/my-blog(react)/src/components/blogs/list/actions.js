import Service from '../service';

export const UPDATE_BLOGS = 'UPDATE_BLOGS';
export const RESET_BLOGS = 'RESET_BLOGS';
export const LOADING_BLOGS = 'LOADING_BLOGS';
export const BLOGS_LOADED = 'BLOGS_LOADED';
export const BLOGS_ERRORS = 'BLOGS_ERRORS';

const service = new Service();

const reset = () => ({
  type: RESET_BLOGS
});

const loading = () => ({
  type: LOADING_BLOGS
});

const loaded = () => ({
  type: BLOGS_LOADED
});

const update = (blogs) => ({
  type: UPDATE_BLOGS,
  payload: blogs
});

const failed = (errors) => ({
  type: BLOGS_ERRORS,
  payload: errors
});

export const load = () => async (dispatch) => {
  dispatch(reset());
  dispatch(loading());
  const response = await service.get();
  dispatch(loaded());

  if (response.success) {
    dispatch(update(response.data));
  } else {
    dispatch(failed(response.data));
  }
};
