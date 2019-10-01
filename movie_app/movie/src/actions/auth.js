import { types } from "./types";
import { LOGIN_API, SIGNUP_API, requestTypes } from "../utils/constants";
import { apiCaller } from "../utils/helpers/api";

const authUserStarted = () => ({
  type: types.AUTH_USER_STARTED
});

const authUserSuccess = state => ({
  type: types.AUTH_USER_SUCCESS,
  payload: {
    user: state.user
  }
});

const authUserFailure = error => ({
  type: types.AUTH_USER_FAILURE,
  payload: {
    error
  }
});

export const logoutUser = () => ({
  type: types.LOGOUT_USER
});

export const loginUser = data => {
  return async dispatch => {
    dispatch(authUserStarted());
    try {
      const response = await apiCaller({
        method: requestTypes.POST,
        url: LOGIN_API,
        data: data
      });
      dispatch(authUserSuccess(response));
    } catch (err) {
      dispatch(authUserFailure(err.message));
    }
  };
};

export const registerUser = data => {
  return async dispatch => {
    if (data.password !== data.confirm_password) {
      dispatch(authUserFailure("Passwords don't match"));
      return;
    }

    dispatch(authUserStarted());
    try {
      const response = await apiCaller({
        method: requestTypes.POST,
        url: SIGNUP_API,
        data: data
      });
      dispatch(authUserSuccess(response));
    } catch (err) {
      dispatch(authUserFailure(err.message));
    }
  };
};
