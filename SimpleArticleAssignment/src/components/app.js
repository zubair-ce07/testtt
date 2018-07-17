import React, { Component } from 'react';

import ArticleList from '../containers/article_list'
import SelectedArticle from '../containers/selected_article'

export default class App extends Component {
    render() {
        return (
            <div>
              <ArticleList />
              <SelectedArticle />
            </div>
        );
    }
}
