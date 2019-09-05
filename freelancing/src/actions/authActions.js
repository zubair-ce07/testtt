import { api } from "../api/api";
import {
  LOGIN_FAILED,
  LOGIN_SUCESS,
  LOGGING_USER,
  FETCH_USER_SUCCESS
} from "./types";
import { API_ROUTES, ROUTES } from "../constants/routes";

export const fetchAuthUser = (token, history) => async dispatch => {
  api.setHeaders({ Authorization: `Token ${token}` });
  const response = await api.get(API_ROUTES.GET_USER);

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

export const loginUser = (creds, history) => async dispatch => {
  // signing in the user started
  dispatch({ type: LOGGING_USER });
  // api request to get token
  const data = JSON.stringify(creds);
  const headers = { "Content-Type": "application/json" };
  const response = await api.post(API_ROUTES.GET_TOKEN, data, { headers });

  if (!response.ok) {
    dispatch({
      type: LOGIN_FAILED,
      payload: response.data.non_field_errors[0]
    });
    return;
  }
  // get user profile using token
  dispatch(fetchAuthUser(response.data.token, history));
};
