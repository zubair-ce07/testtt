

import {combineReducers} from 'redux';
import categories from './categoryReducer';
import comments from './comment';
import posts from './post';

const rootReducer = combineReducers({
    categories,comments,posts
})

export default rootReducer;