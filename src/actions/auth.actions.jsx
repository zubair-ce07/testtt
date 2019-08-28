import faker from "faker";

import {
  LOGIN_ERROR,
  LOGIN_SUCCESS,
  LOGOUT,
  REGISTER_ERROR,
  REGISTER_SUCCESS
} from "./actions.types";
import database from "../apis/database";
import history from "../history";
import { fetchUser } from "./user.actions";

// LOGIN
// ==============================================

export const loginError = message => {
  return {
    type: LOGIN_ERROR,
    payload: { error: message }
  };
};

export const loginSuccess = user_id => {
  return {
    type: LOGIN_SUCCESS,
    payload: user_id
  };
};

export const logout = () => {
  /*
    No real authentication maintained at server side.
    Simulating log in/out using local storage.
  */
  localStorage.clear();
  history.push("/login");
  return {
    type: LOGOUT
  };
};

const verifyTokens = () => {
  const { refresh, access } = retrieveTokens();
  if (!refresh) return false;
};

const retrieveTokens = () => {
  const refresh = localStorage.getItem("refreshToken") || undefined;
  const access = localStorage.getItem("accessToken") || undefined;
  return { refresh, access };
};

const storeTokens = (access, refresh) => {
  localStorage.setItem("accessToken", access);
  localStorage.setItem("refreshToken", refresh);
};

export const loginUser = userCedentials => async dispatch => {
  try {
    const { data } = await database.post(`/login`, userCedentials);
    const { user_id, access, refresh } = data;
    dispatch(loginSuccess(user_id));
    dispatch(fetchUser(user_id));
    storeTokens(access, refresh);
    history.push("/");
  } catch (error) {
    dispatch(loginError(error.data.detail));
  }

  /*
    No real authentication maintained at server side.
    Simulating log in/out using local storage.
  */

  // localStorage.setItem("email", userCedentials.email);
  // localStorage.setItem("password", userCedentials.password);
  /*
    Route to home page after login.
    Some modifications needed in ProfilePage to enable this option here.
    As of now, automatic reroute won't happen.
  */
};

// REGISTER
// ==============================================

export const registerError = message => {
  return {
    type: REGISTER_ERROR,
    payload: { status: "Failure", message }
  };
};

export const registerSuccess = message => {
  return {
    type: REGISTER_SUCCESS,
    payload: { status: "Success", message }
  };
};

export const registerUser = newUser => async dispatch => {
  newUser.display_picture = faker.image.avatar();

  console.log("new user", newUser);
  try {
    await database.post("/register", newUser);
    dispatch(registerSuccess("Account created."));
    setTimeout(() => {
      history.push("/login");
    }, 1000);
  } catch (error) {
    dispatch(registerError(error.data));
  }
};
