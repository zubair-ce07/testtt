import { ADD_MEDIA, REMOVE_MEDIA, CLEAR_MEDIA } from "./actions.types";

export const addMedia = media => {
  return {
    type: ADD_MEDIA,
    payload: media
  };
};

export const removeMedia = media => {
  return {
    type: REMOVE_MEDIA,
    payload: media
  };
};
export const clearMedia = () => {
  return {
    type: CLEAR_MEDIA
  };
};
