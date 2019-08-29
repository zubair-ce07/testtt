import _ from "lodash";
import moment from "moment";

import database from "../apis/database";
import {
  FETCH_FEED,
  CREATE_POST,
  DELETE_POST,
  FETCH_USER_POSTS
} from "./actions.types";
import { fetchUser } from "./user.actions";
import { fetchFollowing } from "./following.actions";

export const fetchFeedAndUsers = () => async (dispatch, getState) => {
  await dispatch(fetchFeed());

  _.chain(getState().posts)
    .map("author")
    .uniq()
    .forEach(id => dispatch(fetchUser(id)))
    .value();
};

export const createPost = post => async (dispatch, getState) => {
  post.author = getState().auth.user_id;
  post.time = moment().format();

  console.log("ima post", post);

  const response = await database.post("/posts/", post);

  dispatch({
    type: CREATE_POST,
    payload: response.data
  });
};

export const fetchUserPosts = user_id => async dispatch => {
  const response = await database.get(`/users/${user_id}/posts/`);
  dispatch({
    type: FETCH_USER_POSTS,
    payload: response.data
  });
};

export const fetchFeed = () => async (dispatch, getState) => {
  const user_id = getState().auth.user_id;

  const response = await database.get(`/feed/${user_id}/`);
  dispatch({
    type: FETCH_FEED,
    payload: response.data
  });
};

export const deletePost = id => async dispatch => {
  await database.delete(`/posts/${id}`);
  dispatch({
    type: DELETE_POST,
    payload: id
  });
};
