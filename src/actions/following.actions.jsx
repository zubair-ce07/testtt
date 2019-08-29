import database from "../apis/database";
import {
  FOLLOW_USER,
  UNFOLLOW_USER,
  FETCH_FOLLOWING
} from "../actions/actions.types";
import { fetchFeed } from "./post.actions";

// FOLLOW
// ==============================================

export const fetchFollowing = () => async (dispatch, getState) => {
  const followerId = getState().auth.user_id;
  const response = await database.get(`/users/${followerId}/followings/`);
  const payload = { followerId, following: response.data };
  dispatch({ type: FETCH_FOLLOWING, payload });
};

export const followUser = followeeId => async (dispatch, getState) => {
  const followerId = getState().auth.user_id;
  const newFollowing = { follower: followerId, followee: followeeId };
  const response = await database.post(`/followings/`, newFollowing);
  dispatch({ type: FOLLOW_USER, payload: response.data });
  dispatch(fetchFeed());
};

export const unfollowUser = followeeId => async (dispatch, getState) => {
  const followerId = getState().auth.user_id;
  const followingId = getState().followings[followerId][followeeId];

  await database.delete(`/followings/${followingId}`);

  const payload = { followerId, followeeId };
  dispatch({ type: UNFOLLOW_USER, payload });
};
