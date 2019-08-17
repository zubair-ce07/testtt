import _ from "lodash";
import moment from "moment";

import database from "../apis/database";
import {
  FETCH_FEED,
  CREATE_POST,
  DELETE_POST,
  FETCH_USER_POSTS
} from "./types";
import { fetchUser } from "./user.action";

export const fetchFeedAndUsers = () => async (dispatch, getState) => {
  await dispatch(fetchFeed());

  _.chain(getState().posts)
    .map("author")
    .uniq()
    .forEach(id => dispatch(fetchUser(id)))
    .value();
};

export const createPost = post => async (dispatch, getState) => {
  post.author = getState().auth.user.id;
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
  const { following } = getState().auth.user;

  if (Object.keys(following).length === 0) {
    return dispatch({
      type: FETCH_FEED,
      payload: []
    });
  }

  let query = "/posts?";

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
