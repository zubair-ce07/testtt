import database from "../apis/database";
import { ADD_FRIEND, REMOVE_FRIEND, FETCH_FRIENDS } from "./actions.types";
import { fetchFeed } from "./post.actions";

// FOLLOW
// ==============================================

export const fetchFriends = () => async (dispatch, getState) => {
  const { user_id } = getState().auth;
  const response = await database.get(`/users/${user_id}/friends/`);
  const payload = { added_by: user_id, friends: response.data };
  dispatch({ type: FETCH_FRIENDS, payload });
};

export const addFriend = friend => async (dispatch, getState) => {
  const { user_id: added_by } = getState().auth;
  const newFriend = { added_by, friend };
  const response = await database.post(`/friends/`, newFriend);
  dispatch({ type: ADD_FRIEND, payload: response.data });
  dispatch(fetchFeed());
};

export const removeFriend = friend => async (dispatch, getState) => {
  const { user_id: added_by } = getState().auth;
  const friendshipID = getState().followings[added_by][friend];

  await database.delete(`/friends/${friendshipID}`);

  const payload = { added_by, friend };
  dispatch({ type: REMOVE_FRIEND, payload });
};
