import Service from './service';

export const UPDATE_COMMENTS = 'UPDATE_COMMENTS';
export const RESET_COMMENTS = 'RESET_COMMENTS';
export const LOADING_COMMENTS = 'LOADING_COMMENTS';
export const COMMENTS_LOADED = 'COMMENTS_LOADED';
export const COMMENTS_ERRORS = 'COMMENTS_ERRORS';

const service = new Service();

const reset = () => ({
  type: RESET_COMMENTS
});

const loading = () => ({
  type: LOADING_COMMENTS
});

const loaded = () => ({
  type: COMMENTS_LOADED
});

const update = (fields) => ({
  type: UPDATE_COMMENTS,
  payload: fields
});

const failed = (errors) => ({
  type: COMMENTS_ERRORS,
  payload: errors
});

export const load = blogId => async (dispatch) => {
  dispatch(reset());
  dispatch(loading());
  const response = await service.get({ blog_id: blogId });
  dispatch(loaded());

  if (response.success) {
    dispatch(update(response.data));
  } else {
    dispatch(failed(response.data));
  }
};

export const addComment = comment => async (dispatch, getState) => {
  const state = getState();

  dispatch(loading());
  const response = await service.add(comment);
  dispatch(loaded());

  if (response.success) {
    const comments = state.CommentsReducer.comments;
    dispatch(update([...comments, response.data]));
  } else {
    dispatch(failed(response.data));
  }
};

export const addReply = comment => async (dispatch, getState) => {
  let comments = getState().CommentsReducer.comments;

  dispatch(loading());
  const responsePromise = service.add(comment);
  const commentPath = findCommentPath(comments, comment.object_id);
  const response = await responsePromise;
  dispatch(loaded());

  if (response.success) {
    comments = addReplyToComments(commentPath, comments, response.data);
    dispatch(update(comments));
  } else {
    dispatch(failed(response.data));
  }
};

const findCommentPath = (comments, id) => {
  if (comments) {
    for (let i = 0; i < comments.length; i++) {
      if (comments[i].id === id) {
        return [i];
      }
      let found = findCommentPath(comments[i].comments, id);
      if (found && found.push(i)) return found;
    }
  }
};

const addReplyToComments = (path, comments, comment) => {
  const index = path.pop();

  return [
    ...comments.slice(0, index),
    {
      ...comments[index],
      comments: path.length ?
        addReplyToComments(path, comments[index].comments, comment) :
        [...comments[index].comments, comment]
    },
    ...comments.slice(index + 1)
  ];
};
