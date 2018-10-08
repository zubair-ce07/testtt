import { connect } from 'react-redux';
import { NotificationManager } from 'react-notifications';

import { CLEAR_USER, UPDATE_USER } from '../../consts';
import UsersService from './service';

import history from '../../history';

const usersService = new UsersService();

const updateUser = fields => ({
  type: UPDATE_USER,
  payload: fields
});

const clearUser = () => ({
  type: CLEAR_USER
});

const updateField = (name, value, required) => {
  return (dispatch, getState) => {
    const errors = { ...getState().user.errors };

    errors[name] = [];
    if (required && !value) {
      errors[name].push('This field can\'t be empty');
    }

    dispatch(updateUser({ [name]: value, errors }));
  };
};

const matchPassword = () => {
  return (dispatch, getState) => {
    const { errors, password, confirm_password } = getState().user;
    errors.confirm_password = [];
    if (confirm_password && password !== confirm_password) {
      errors.confirm_password
        .push('Password and confirm password are not same');
    }
    dispatch(updateUser({ errors }));
  };
};

const saveUser = () => {
  return async (dispatch, getState) => {
    const { errors, ...user } = getState().user;

    dispatch(matchPassword());
    if (Object.keys(errors).some(key => errors[key].length)) {
      return;
    }

    let response = null;

    if (user.id) {
      if (!user.password) {
        delete user.password;
      }
      response = await usersService.update(user);
    } else {
      response = await usersService.register(user);
    }

    if (response.success) {
      if (user.id) {
        localStorage.setItem('user', JSON.stringify(user));
        NotificationManager.success('Updated successfully');
        dispatch(updateUser({
          ...response.data,
          errors: {},
          password: '',
          confirm_password: ''
        }));
      } else {
        NotificationManager.success('Registered successfully');
        history.push('/users/signin');
        dispatch(clearUser());
      }
    } else {
      dispatch(updateUser({ errors: response.data }));
    }
  };
};

const sigIn = (username, password) => {
  return async (dispatch) => {
    const response = await usersService.login({ username, password });
    if (response.success) {
      history.push('/blogs');
      localStorage.setItem('user', JSON.stringify(response.data));
      dispatch(updateUser({ ...response.data, errors: {} }));
    } else if (response.code === 404) {
      dispatch(updateUser({ errors: { password: true } }));
    }
  };
};

const sigOut = () => {
  return (dispatch) => {
    localStorage.clear();
    history.push('/');
    dispatch(clearUser());
  };
};

const mapStateToProps = state => ({
  user: state.user
});

const mapDispatchToProps = dispatch => ({
  updateField: (name, value, required) => dispatch(updateField(name, value, required)),
  matchPassword: () => dispatch(matchPassword()),
  saveUser: () => dispatch(saveUser()),
  signIn: (username, password) => dispatch(sigIn(username, password)),
  signOut: () => dispatch(sigOut()),
});


export default connect(mapStateToProps, mapDispatchToProps);
