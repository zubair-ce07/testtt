import { NotificationManager } from 'react-notifications';

import Service from '../service';
import history from '../../../history';

export const UPDATE_BLOG = 'UPDATE_BLOG';
export const RESET_BLOG = 'RESET_BLOG';
export const LOADING_BLOG = 'LOADING_BLOG';
export const BLOG_LOADED = 'BLOG_LOADED';
export const BLOG_ERRORS = 'BLOG_ERRORS';

const service = new Service();

export const reset = () => ({
  type: RESET_BLOG
});

const loading = () => ({
  type: LOADING_BLOG
});

const loaded = () => ({
  type: BLOG_LOADED
});

const update = (fields) => ({
  type: UPDATE_BLOG,
  payload: fields
});

const failed = (errors) => ({
  type: BLOG_ERRORS,
  payload: errors
});

export const updateField = (name, value) => update({ [name]: value });

export const addTag = (tag) => (dispatch, getState) => {
  let tags = getState().CreateBlogReducer.blog.tags;

  tags = [...tags, tag];

  dispatch(update({ tags }));
};

export const removeTag = index => (dispatch, getState) => {
  let tags = getState().CreateBlogReducer.blog.tags;

  tags = [
    ...tags.slice(0, index),
    ...tags.slice(index + 1)
  ];

  dispatch(update({ tags }));
};

export const save = () => async (dispatch, getState) => {
  const blog = getState().CreateBlogReducer.blog;
  let response = null;

  dispatch(loading());

  if (blog.id) {
    response = await service.update(blog.id, blog);
  } else {
    response = await service.add(blog);
  }

  dispatch(loaded());

  if (response.success) {

    NotificationManager.success(
      `Blog ${blog.id ? 'updated' : 'created'} successfully`);

    history.push(`/blogs/${response.data.id}`);
    dispatch(reset());
  } else {
    dispatch(failed(response.data));
  }
};

export const load = id => async (dispatch) => {
  dispatch(reset());
  dispatch(loading());
  const response = await service.getById(id);
  dispatch(loaded());

  if (response.success) {
    dispatch(update(response.data));
  } else {
    dispatch(failed(response.data));
  }
};
