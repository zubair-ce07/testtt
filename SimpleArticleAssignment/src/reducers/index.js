import { combineReducers } from 'redux';
import ArticleList from './article_reducer'
import Article from './selected_article_reducer'

const rootReducer = combineReducers({
    articles: ArticleList,
    selectedArticle: Article
});

export default rootReducer;
