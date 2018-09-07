import React, {Component} from 'react';
import { Row, Col, Grid, Thumbnail, Button, ListGroup, ListGroupItem } from 'react-bootstrap';
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
      <div>
        <ul className="col-md-8 list-group">
          {AllArticles}
        </ul>

        <article className="col-sm-4">
          <h3 className="text-left">Top Headlines</h3>
        </article>

        
      </div>
    );
}


export default ArticleList;
