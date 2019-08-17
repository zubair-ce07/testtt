import _ from "lodash";
import {
  FETCH_USER,
  FETCH_ALL_USERS,
  FOLLOW_USER,
  UNFOLLOW_USER
} from "../actions/types";

const INITIAL_STATE = {};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case FETCH_USER:
      return { ...state, [action.payload.id]: action.payload };
    case FETCH_ALL_USERS:
      return { ...state, ..._.mapKeys(action.payload, "id") };
    case FOLLOW_USER: {
      const { followerId, userId } = action.payload;
      const follower = state[followerId];
      const oldFollowing = follower.following;
      const newState = {
        ...state,
        [followerId]: {
          ...follower,
          following: { ...oldFollowing, [userId]: true }
        }
      };
      return newState;
    }
    case UNFOLLOW_USER: {
      const { followerId, userId } = action.payload;
      const follower = state[followerId];
      const oldFollowing = follower.following;
      const newState = {
        ...state,
        [followerId]: {
          ...follower,
          following: _.omit(oldFollowing, userId)
        }
      };
      return newState;
    }
    default:
      return state;
  }
};
