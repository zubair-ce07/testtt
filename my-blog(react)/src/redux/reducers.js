import { combineReducers } from 'redux';

import { CreateBlogReducer } from '../components/blogs/create';
import { BlogsListReducer } from '../components/blogs/list';
import { BlogDetailReducer } from '../components/blogs/detail';
import { TagsReducer } from '../components/blogs/tags';
import { CommentsReducer } from '../components/blogs/comments';
import { UserReducer } from '../components/users/create/reducer';
export default combineReducers({
  CreateBlogReducer,
  TagsReducer,
  BlogsListReducer,
  BlogDetailReducer,
  CommentsReducer,
  UserReducer,
});
