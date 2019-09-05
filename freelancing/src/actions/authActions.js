import { api } from "../api/api";
import {
  LOGIN_FAILED,
  LOGIN_SUCESS,
  LOGGING_USER,
  FETCH_USER_SUCCESS,
  LOGOUT_USER
} from "./types";
import { API_ROUTES, ROUTES } from "../constants/routes";

export const loginUser = (creds, history) => async dispatch => {
  // signing in the user started
  dispatch({ type: LOGGING_USER });
  // api request to get token
  const data = JSON.stringify(creds);
  const headers = { "Content-Type": "application/json" };
  let response = await api.post(API_ROUTES.GET_TOKEN, data, { headers });

  if (!response.ok) {
    dispatch({
      type: LOGIN_FAILED,
      payload: "login failed"
    });
    return;
  }
  // get user profile using token
  const token = response.data.token;
  api.setHeaders({ Authorization: `Token ${token}` });
  response = await api.get(API_ROUTES.USERS);

  if (!response.ok) {
    dispatch({
      type: LOGIN_FAILED,
      payload: "error fetching the user profile"
    });
    return;
  }

  dispatch({ type: FETCH_USER_SUCCESS, payload: response.data });
  dispatch({ type: LOGIN_SUCESS, payload: { token, uid: response.data.id } });
  // redirect to buyer dashboard
  history.replace(ROUTES.ROOT);
};

export const registerUser = (user, history) => async dispatch => {
  // signing in the user started
  dispatch({ type: LOGGING_USER });
  // api request to get token
  const data = JSON.stringify(user);
  const headers = { "Content-Type": "application/json" };
  const response = await api.post(API_ROUTES.REGISTER, data, { headers });

  if (!response.ok) {
    dispatch({
      type: LOGIN_FAILED,
      payload: "registration failed"
    });
    return;
  }
  // logging user after successful registration
  const creds = {
    username: user.username,
    password: user.password
  };
  dispatch(loginUser(creds, history));
};

export const logoutUser = () => dispatch => {
  dispatch({ type: LOGOUT_USER });
};
