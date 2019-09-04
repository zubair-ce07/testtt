import _ from "lodash";

import {
  FETCH_FRIENDS,
  ADD_FRIEND,
  REMOVE_FRIEND
} from "../actions/actions.types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_FRIENDS: {
      return {
        ...state,
        [action.payload.added_by]: indexById(action.payload.friends)
      };
    }
    case ADD_FRIEND: {
      const { added_by, friend, id } = action.payload;
      const oldFollowing = state[added_by];
      const newState = {
        ...state,
        [added_by]: {
          ...oldFollowing,
          [friend]: id
        }
      };
      return newState;
    }
    case REMOVE_FRIEND: {
      const { added_by, friend } = action.payload;
      const oldFriendList = state[added_by];
      const newState = {
        ...state,
        [added_by]: {
          ..._.omit(oldFriendList, friend)
        }
      };
      return newState;
    }
    default:
      return state;
  }
};

const indexById = array => {
  return array.reduce((dictionary, friendlist) => {
    dictionary[friendlist["friend"]] = friendlist["id"];
    return dictionary;
  }, {});
};
