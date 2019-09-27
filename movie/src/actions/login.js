import axios from "axios";
import { types } from "./types";
import { LOGIN_API } from "../utils/constants";

const loginUserStarted = () => ({
  type: types.LOGIN_USER_STARTED
});

const loginUserSuccess = user => ({
  type: types.LOGIN_USER_SUCCESS,
  payload: {
    user
  }
});

const loginUserFailure = error => ({
  type: types.LOGIN_USER_fAILURE,
  payload: {
    error
  }
});

export const loginUser = ({ email, password }) => {
  return dispatch => {
    dispatch(loginUserStarted());
    axios
      .post(LOGIN_API, { email, password })
      .then(res => dispatch(loginUserSuccess(res.data)))
      .catch(err => dispatch(loginUserFailure(err.message)));
  };
};
