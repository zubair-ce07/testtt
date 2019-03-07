import { NotificationManager } from 'react-notifications';

import Service from '../service';
import history from '../../../history';

export const UPDATE_USER = 'UPDATE_USER';
export const RESET_USER = 'RESET_USER';
export const LOADING_USER = 'LOADING_USER';
export const USER_LOADED = 'USER_LOADED';
export const USER_ERRORS = 'USER_ERRORS';

const service = new Service();

export const reset = () => ({
  type: RESET_USER
});

export const loading = () => ({
  type: LOADING_USER
});

export const loaded = () => ({
  type: USER_LOADED
});

export const update = (fields) => ({
  type: UPDATE_USER,
  payload: fields
});

export const failed = (errors) => ({
  type: USER_ERRORS,
  payload: errors
});

export const updateField = (name, value, required) => (dispatch, getState) => {
  const errors = { ...getState().UserReducer.errors };

  errors[name] = [];
  if (required && !value) {
    errors[name].push('This field can\'t be empty');
  }

  dispatch(failed(errors));
  dispatch(update({ [name]: value }));
};

export const matchPassword = () => (dispatch, getState) => {
  const {
    errors: { ...errors },
    user: { password, confirm_password }
  } = getState().UserReducer;

  errors.confirm_password = [];
  if (confirm_password && password !== confirm_password) {
    errors.confirm_password
      .push('Password and confirm password are not same');
  }
  dispatch(failed(errors));
};

export const save = () => async (dispatch, getState) => {
  const { user, errors } = getState().UserReducer;
  dispatch(matchPassword());
  if (user.password !== user.confirm_password ||
    Object.keys(errors).some(key => errors[key].length)
  ) {
    return;
  }
  let response = null;

  dispatch(loading());
  if (user.id) {
    if (!user.password) {
      delete user.password;
    }
    response = await service.update(user);
  } else {
    response = await service.register(user);
  }
  dispatch(loaded());

  if (response.success) {

    if (user.id) {
      NotificationManager.success('User updated successfully');
    } else {
      NotificationManager.success('User registered successfully');
      history.push('/users/signin');
      dispatch(reset());
    }
  } else {
    dispatch(failed(response.data));
  }
};

export const loadSignedInUser = () => async (dispatch) => {
  dispatch(loading());
  const response = await service.getSignedInUser();
  dispatch(loaded());

  if (response.success) {
    localStorage.setItem('user', JSON.stringify(response.data));
    dispatch(update(response.data));
  } else {
    history.push('/users/signin');
    dispatch(reset());
  }
};
