import faker from "faker";
import _ from "lodash";

import {
  LOGIN_ERROR,
  LOGIN_SUCCESS,
  LOGOUT,
  REGISTER_ERROR,
  REGISTER_SUCCESS,
  FETCH_USER,
  FETCH_ALL_USERS,
  FOLLOW_USER,
  UNFOLLOW_USER
} from "./types";
import database from "../apis/database";
import history from "../history";

// FETCH
// ==============================================

export const fetchUser = id => async dispatch => {
  const response = await database.get(`/users/${id}`);
  dispatch({ type: FETCH_USER, payload: response.data });
};

export const fetchAllUsers = () => async dispatch => {
  const response = await database.get("/users");
  dispatch({ type: FETCH_ALL_USERS, payload: response.data });
};

// LOGIN
// ==============================================

export const loginError = message => {
  return {
    type: LOGIN_ERROR,
    payload: { error: message }
  };
};

export const loginSuccess = userId => {
  return {
    type: LOGIN_SUCCESS,
    payload: userId
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

export const loginUser = userCedentials => async dispatch => {
  const response = await database.get(`/users?email=${userCedentials.email}`);

  if (response.data.length === 0) {
    dispatch(loginError("Email not registered."));
    return;
  }

  const userDetails = response.data[0];

  if (userDetails.password !== userCedentials.password) {
    dispatch(loginError("Incorrect password."));
    return;
  }

  dispatch(loginSuccess(userDetails));
  dispatch({ type: FETCH_USER, payload: userDetails });

  /*
    No real authentication maintained at server side.
    Simulating log in/out using local storage.
  */
  localStorage.setItem("email", userCedentials.email);
  localStorage.setItem("password", userCedentials.password);

  /*
    Route to home page after login.
    Some modifications needed in ProfilePage to enable this option here.
    As of now, automatic reroute won't happen.
  */
  history.push("/");
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
  const existingUser = await database.get(`/users?email=${newUser.email}`);

  if (existingUser.data.length > 0) {
    dispatch(registerError("Email already registered."));
    return;
  }

  newUser.displayPicture = faker.image.avatar();

  database.post("/users", newUser);

  dispatch(registerSuccess("Account created."));
  setTimeout(() => {
    history.push("/login");
  }, 1000);
};

// FOLLOW
// ==============================================

export const followUser = userId => async (dispatch, getState) => {
  const followerId = getState().auth.user.id;
  const oldFollowing = getState().auth.user.following;

  const following = { ...oldFollowing, [userId]: true };

  await database.patch(`/users/${followerId}`, { following });

  const payload = { followerId, userId };
  dispatch({ type: FOLLOW_USER, payload });
};

export const unfollowUser = userId => async (dispatch, getState) => {
  const followerId = getState().auth.user.id;
  const oldFollowing = getState().auth.user.following;

  const following = _.omit(oldFollowing, userId);

  await database.patch(`/users/${followerId}`, { following });

  const payload = { followerId, userId };
  dispatch({ type: UNFOLLOW_USER, payload });
};
