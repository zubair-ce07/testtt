import djangoapi from "./djangoapi.js";
import utils from "./utils";

export const GET_PROFILE_START = "GET_PROFILE_START";
export const getProfileStart = username => {
  return dispatch => {
    return djangoapi.getProfile(username, jsonData => {
      dispatch(getProfileEnd(jsonData));
    });
  };
};

export const GET_PROFILE_END = "GET_PROFILE_END";
export const getProfileEnd = jsonData => {
  return {
    type: GET_PROFILE_END,
    profile: jsonData
  };
};

export const REPLACE_DIRECTS_START = "REPLACE_DIRECTS_START";
export const replaceDirectsStart = (username, hierarchy) => {
  return dispatch => {
    return djangoapi.getDirects(username, jsonData => {
      hierarchy = utils.replaceDirects(username, hierarchy, jsonData.directs);
      dispatch(replaceDirectsEnd(hierarchy));
    });
  };
};

export const REPLACE_DIRECTS_END = "REPLACE_DIRECTS_END";
export const replaceDirectsEnd = hierarchy => {
  return {
    type: REPLACE_DIRECTS_END,
    hierarchy
  };
};
