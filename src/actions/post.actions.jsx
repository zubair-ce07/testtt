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
  post.author = getState().auth.userId;
  post.time = moment().format();

  const response = await database.post("/posts", post);

  dispatch({
    type: CREATE_POST,
    payload: response.data
  });
};

export const fetchUserPosts = userId => async dispatch => {
  const response = await database.get(`/posts?author=${userId}`);
  dispatch({
    type: FETCH_USER_POSTS,
    payload: response.data
  });
};

export const fetchFeed = () => async (dispatch, getState) => {
  const userId = getState().auth.userId;
  await dispatch(fetchFollowing(userId));

  const following = getState().followings[userId];

  /**
   * This step is server's responsibility but since we have
   * a thin server, it's been done here
   */

  let query = "/posts?";
  query += `author=${userId}&`;

  Object.keys(following).forEach(k => {
    if (following[k]) {
      query += `author=${k}&`;
    }
  });

  query += "_sort=id&_order=desc";

  const response = await database.get(query);
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
