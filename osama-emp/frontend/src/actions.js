import djangoapi from "./djangoapi.js";

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
