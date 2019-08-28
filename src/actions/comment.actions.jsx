import _ from "lodash";
import moment from "moment";

import database from "../apis/database";
import { CREATE_COMMENT, FETCH_COMMENTS } from "./actions.types";
import { fetchUser } from "./user.actions";

export const fetchCommentsAndUsers = postId => async (dispatch, getState) => {
  await dispatch(fetchComments(postId));

  _.chain(getState().posts)
    .map("author")
    .uniq()
    .forEach(id => dispatch(fetchUser(id)))
    .value();
};

export const fetchComments = postId => async dispatch => {
  const response = await database.get(`/comments/?post=${postId}`);
  const payload = {
    comments: response.data,
    postId
  };

  dispatch({ type: FETCH_COMMENTS, payload });
};

export const createComment = (comment, postId) => async (
  dispatch,
  getState
) => {
  comment.author = getState().auth.user_id;
  comment.time = moment().format();
  comment.post = postId;

  console.log("ima comment", comment);

  const response = await database.post("/comments/", comment);

  const payload = {
    comment: response.data,
    postId
  };

  dispatch({ type: CREATE_COMMENT, payload });
};
