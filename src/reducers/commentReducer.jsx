import _ from "lodash";
import { CREATE_COMMENT, FETCH_COMMENTS } from "../actions/actions.types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case CREATE_COMMENT: {
      const newState = _.cloneDeep(state);
      const { postId } = action.payload;
      if (newState[postId] === undefined) newState[postId] = [];
      newState[postId].push(action.payload.comment);
      return newState;
    }
    case FETCH_COMMENTS: {
      const newState = _.cloneDeep(state);
      newState[action.payload.postId] = action.payload.comments;
      return { ...newState };
    }
    default:
      return state;
  }
};
