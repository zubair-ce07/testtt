import axios from 'axios';

export const FETCH_ARTICLES_LIST = "ARTICLE_LIST";
export const SELECT_ARTICLE = "ARTICLE_SELECTED";

export function getArticleList () {

    let articlesUrl = 'http://127.0.0.1:8000/articles/articles/';
    return {
        type: FETCH_ARTICLES_LIST,
        payload: axios.get(articlesUrl)
    };

}
export function selectArticle (article) {
    return {
        type: SELECT_ARTICLE,
        payload: article
    };
}
