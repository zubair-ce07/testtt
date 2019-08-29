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

export const loginSuccess = (user_id, access) => {
  return {
    type: LOGIN_SUCCESS,
    payload: { user_id, access }
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

export const attemptLogin = () => async dispatch => {
  try {
    const { user_id, refresh } = retrieveAuthDetails();
    if (!user_id || !refresh) return;

    const { access } = await database.post("/login/refresh", { refresh });
    dispatch(loginSuccess(user_id, access));
  } catch (error) {
    // console.log("error", error);
  }
};

const retrieveAuthDetails = () => {
  const user_id = localStorage.getItem("user_id") || undefined;
  const refresh = localStorage.getItem("refreshToken") || undefined;
  return { user_id, refresh };
};

const storeAuthDetails = (user_id, refresh) => {
  localStorage.setItem("user_id", user_id);
  localStorage.setItem("refreshToken", refresh);
};

export const loginUser = userCedentials => async dispatch => {
  try {
    const { data } = await database.post(`/login`, userCedentials);
    const { user_id, access, refresh } = data;
    dispatch(loginSuccess(user_id, access));
    storeAuthDetails(user_id, refresh);
    dispatch(fetchUser(user_id));
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
