import { SEARCH_YOUTUBE, END_SEARCH_REQUEST, PLAY_VIDEO } from "./actions";

const initialState = {
  playVid: false,
  vidId: "",
  results: []
};

const rootReducer = (state = initialState, action) => {
  switch (action.type) {
    case SEARCH_YOUTUBE:
      return state;
    case END_SEARCH_REQUEST:
      return Object.assign({}, state, {
        results: action.results
      });
    case PLAY_VIDEO:
      return Object.assign({}, state, {
        playVid: true,
        vidId: action.vidId
      });
    default:
      return state;
  }
};

export default rootReducer;
