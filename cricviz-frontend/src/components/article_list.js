import React, {Component} from 'react';
import { Row, Col, Grid, Thumbnail, Button } from 'react-bootstrap';
import ArticleListItem from './article_list_item';

const ArticleList = (props) => {
  const AllArticles = props.articles.map((article) => {
    return (
      <ArticleListItem
        key={article.url}
        article={article} />
      );
    });

    return (
      <ul className="col-md-8 list-group">
        {AllArticles}
      </ul>
    );
}


export default ArticleList;
