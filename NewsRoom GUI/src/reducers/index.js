import { combineReducers } from 'redux';
import TopNewsReducer from './reducer_top_news';
import DetailNewsReducer from './reducer_detail_news';
import OtherNewsReducer from './reducer_category_news';
import SearchNewsReducer from './reducer_search_news';
import UserReducer from './reducer_user'
import { reducer as formReducer } from 'redux-form';

const rootReducer = combineReducers({
  top_news: TopNewsReducer,
  selected_news: DetailNewsReducer,
  otherNews: OtherNewsReducer,
  searchNews: SearchNewsReducer,
  form: formReducer,
  user: UserReducer
});

export default rootReducer;
