import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

import BlogsReducer from './reducer_blogs';
import BlogDetailsReducer from './reducer_blog_details';

const rootReducer = combineReducers({
    blogs: BlogsReducer,
    blog_details: BlogDetailsReducer,
    form: formReducer
});

export default rootReducer;
