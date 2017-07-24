export const SEARCH_YOUTUBE = "SEARCH_YOUTUBE";

export const searchYoutube = query => {
  return {
    type: SEARCH_YOUTUBE,
    query
  };
};
