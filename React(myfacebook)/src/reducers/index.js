import { combineReducers } from 'redux';
import newsListReducer from '../reducers/NewsListReducer';
import newsDetailReducer from '../reducers/NewsDetailReducer'

const rootReducer = combineReducers({
    newsListReducer,
    newsDetailReducer
});

export default rootReducer;
