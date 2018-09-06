import React from 'react';
import { Row, Col, Grid, Thumbnail, Button } from 'react-bootstrap';

const ArticleListItem = (props) => {
  const article = props.article;

  if(!article) {
    return <div>Article Not found</div>;
  }

  const url = article.url;
  const title = article.title;
  const description = article.description;

  return (
    <li className="list-group-item">
      <div>
        <Row>
          <Col xs={6} md={8}>
            <Thumbnail src={url} alt="242x200">
              <h3>{title}</h3>
              <p>{description}</p>
              <p>
                <Button bsStyle="primary">Read full article</Button>
              </p>
            </Thumbnail>
          </Col>
        </Row>
      </div>
    </li>
  );
}

export default ArticleListItem;
