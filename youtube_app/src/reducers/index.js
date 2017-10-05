import { combineReducers } from 'redux'
import videoList from './videoList'
import selectedVideo from './selectedVideo'

const youtubeApp = combineReducers({
    videoList,
    selectedVideo
});

export default youtubeApp;
