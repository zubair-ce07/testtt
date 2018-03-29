

import {combineReducers} from 'redux';
import categories from './category';
import posts from './post';

const rootReducer = combineReducers({
    categories,posts
})

export default rootReducer;