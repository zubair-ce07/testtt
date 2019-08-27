import { FETCH_USER, FETCH_ALL_USERS } from "./actions.types";
import database from "../apis/database";

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
