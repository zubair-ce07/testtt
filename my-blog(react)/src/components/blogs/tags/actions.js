import Service from './service';

export const UPDATE_TAGS = 'UPDATE_TAGS';
export const RESET_TAGS = 'RESET_TAGS';
export const LOADING_TAGS = 'LOADING_TAGS';
export const TAGS_LOADED = 'TAGS_LOADED';
export const TAGS_ERRORS = 'TAGS_ERRORS';

const service = new Service();

const reset = () => ({
  type: RESET_TAGS
});

const loading = () => ({
  type: LOADING_TAGS
});

const loaded = () => ({
  type: TAGS_LOADED
});

const update = (tags) => ({
  type: UPDATE_TAGS,
  payload: tags
});

const failed = (errors) => ({
  type: TAGS_ERRORS,
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
