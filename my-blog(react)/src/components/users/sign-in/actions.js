import Service from '../service';
import history from '../../../history';

import { update, failed, reset, loading, loaded } from '../create/actions';

const service = new Service();

const invalidCredentials = () => (dispatch, getState) => {
  const errors = { ...getState().UserReducer.errors };
  errors.confirm_password = ['Username or password is incorrect'];
  dispatch(failed(errors));
};

const signedIn = user => dispatch => {
  localStorage.setItem('user', JSON.stringify(user));
  dispatch(failed({}));
  dispatch(update(user));
};

export const signIn = (username, password) => async dispatch => {
  dispatch(reset);
  dispatch(loading);
  const response = await service.signIn({ username, password });
  dispatch(loaded);
  if (response.success) {
    dispatch(signedIn(response.data));
    history.push('/blogs');
  } else if (response.code === 401) {
    dispatch(invalidCredentials());
  }
};
