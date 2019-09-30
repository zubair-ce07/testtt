import axios from "axios";
import { types } from "./types";
import { LOGIN_API, SIGNUP_API } from "../utils/constants";

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

export const loginUser = ({ email, password }) => {
  return dispatch => {
    dispatch(authUserStarted());
    axios
      .post(LOGIN_API, { email, password })
      .then(res => dispatch(authUserSuccess(res.data)))
      .catch(err => dispatch(authUserFailure(err.message)));
  };
};

export const registerUser = ({
  first_name,
  last_name,
  email,
  password,
  confirm_password,
  gender,
  date_of_birth
}) => {
  return dispatch => {
    if (password !== confirm_password) {
      dispatch(authUserFailure("Passwords don't match"));
      return;
    }
    dispatch(authUserStarted());
    axios
      .post(SIGNUP_API, {
        email,
        password,
        first_name,
        last_name,
        gender,
        date_of_birth
      })
      .then(res => dispatch(authUserSuccess(res.data)))
      .catch(err => dispatch(authUserFailure(err.message)));
  };
};
