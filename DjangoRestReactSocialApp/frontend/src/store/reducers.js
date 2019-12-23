import { combineReducers } from 'redux'

import user from './modules/user/user.reducer'
import post from './modules/post/post.reducer'

export default combineReducers({
  user,
  post
})
