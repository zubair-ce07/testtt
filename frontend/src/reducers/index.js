

import {combineReducers} from 'redux';
import data from './categoryReducer';
import posts from './postReducer';

const rootReducer = combineReducers({
    data
})

export default rootReducer;