import * as youtube from "./youtubeapi";

export const SEARCH_YOUTUBE = "SEARCH_YOUTUBE";

export const searchYoutube = query => {
  return {
    type: SEARCH_YOUTUBE,
    query
  };
};

export const START_REQUEST = "START_REQUEST";
export const startRequest = query => {
  return dispatch => {
    return youtube.search(query).then(jsonData => {
      dispatch(endRequest(jsonData));
    });
    // .catch(error => error);
  };
};

export const END_REQUEST = "END_REQUEST";
export const endRequest = jsonData => {
  return {
    type: END_REQUEST,
    results: jsonData.items
  };
};
