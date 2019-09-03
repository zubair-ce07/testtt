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

export const fetchFeedAndUsers = () => async (dispatch, getState) => {
  await dispatch(fetchFeed());

  _.chain(getState().posts)
    .map("author")
    .uniq()
    .forEach(id => dispatch(fetchUser(id)))
    .value();
};

export const createPost = (post, mediaToUpload) => async (
  dispatch,
  getState
) => {
  post.author = getState().auth.user_id;
  post.time = moment().format();

  const { data: newPost } = await database.post("/posts/", post);

  const uploadedMedia = await Promise.all(
    mediaToUpload.map(async image => {
      const data = new FormData();
      data.append("file_name", image);
      data.append("post", newPost.id);
      const { data: uploadedImage } = await database.post(
        "/posts-media/",
        data
      );
      return uploadedImage.file_name;
    })
  );

  newPost.media = uploadedMedia;

  dispatch({
    type: CREATE_POST,
    payload: newPost
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

  const posts = await Promise.all(
    response.data.map(async post => {
      const mediaResponse = await database.get(`/posts/${post.id}/media/`);
      const media = mediaResponse.data.map(images => images.file_name);
      post.media = media;
      return post;
    })
  );

  dispatch({
    type: FETCH_FEED,
    payload: posts
  });
};

export const deletePost = id => async dispatch => {
  await database.delete(`/posts/${id}`);
  dispatch({
    type: DELETE_POST,
    payload: id
  });
};
