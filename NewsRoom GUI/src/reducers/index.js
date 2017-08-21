import { combineReducers } from 'redux';
import TopNewsReducer from './reducer_top_news';
import DetailNewsReducer from './reducer_detail_news';
import OtherNewsReducer from './reducer_category_news';
import NewsListReducer from './reducer_news_list';
import UserReducer from './reducer_user';
import InterestsReducer from './reducer_user_interests';
import CategoriesReducer from './reducer_all_categories';
import TokenReducer from './reducer_token';
import { reducer as formReducer } from 'redux-form';

const rootReducer = combineReducers({
  top_news: TopNewsReducer,
  selected_news: DetailNewsReducer,
  otherNews: OtherNewsReducer,
  newsList: NewsListReducer,
  form: formReducer,
  user: UserReducer,
  userInterests: InterestsReducer,
  categories: CategoriesReducer,
  token: TokenReducer
});

export default rootReducer;
