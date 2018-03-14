

import {combineReducers} from 'redux';
import weather from './weatherReducer';

const rootReducer = combineReducers({
    // short hand property names
    weather
})

export default rootReducer;