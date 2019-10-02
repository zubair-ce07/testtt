import { types } from "./types";
import { LOGIN_API, SIGNUP_API, requestTypes } from "../utils/constants";
import { apiCaller } from "../utils/helpers/api";

const authUserStarted = () => ({
  type: types.AUTH_USER_STARTED
});

const authUserSuccess = ({user}) => ({
  type: types.AUTH_USER_SUCCESS,
  payload: {
    user
  }
});

export const authUserFailure = error => ({
  type: types.AUTH_USER_FAILURE,
  payload: {
    error
  }
});

export const logoutUser = () => ({
  type: types.LOGOUT_USER
});

export const loginUser = data => {
  return dispatch => {
    dispatch(authUserStarted());
    apiCaller({
      method: requestTypes.POST,
      url: LOGIN_API,
      data
    })
      .then(response => dispatch(authUserSuccess(response.data)))
      .catch(error => dispatch(authUserFailure(error.message)));
  };
};

export const registerUser = data => {
  return dispatch => {
    dispatch(authUserStarted());
    apiCaller({
      method: requestTypes.POST,
      url: SIGNUP_API,
      data
    })
      .then(response => dispatch(authUserSuccess(response.data)))
      .catch(err => dispatch(authUserFailure(err.message)));
  };
};
