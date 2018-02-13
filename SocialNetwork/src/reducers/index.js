import { combineReducers } from 'redux';
import authReducer from './auth';
import postReducer from './post'
import commentReducer from './comment'
import likeReducer from './like'
import friendReducer from './friend'
import userReducer from './user'

 
const rootReducer = combineReducers({
  authReducer,
  postReducer,
  commentReducer,
  friendReducer,
  userReducer,
  likeReducer,
});
 
export default rootReducer;