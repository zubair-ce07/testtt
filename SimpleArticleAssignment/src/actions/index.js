import axios from 'axios';


export function getArticleList () {

    const url = 'http://127.0.0.1:8000/articles/api/articles_list/';
    const request = axios.get(url);
    return {
        type: "ARTICLE_LIST",
        payload: request
    };

}
export function selectArticle (article) {

    return {
        type: "ARTICLE_SELECTED",
        payload: article
    };

}

