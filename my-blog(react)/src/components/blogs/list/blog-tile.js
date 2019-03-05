import React from 'react';
import { Link } from 'react-router-dom';

import { Col } from 'reactstrap';

import { BLOG_TILE_DESCRIPTION_LENGTH } from '../../../constants';
import Tag from '../tags/tag';

const truncateString = (str, length = BLOG_TILE_DESCRIPTION_LENGTH) => {
  if (str.length <= length) {
    return str;
  }

  return str.slice(0, str.lastIndexOf(' ', length)) + '...';
};

const BlogTile = ({ blog: { id, title, body, tags } }) => (
  <Col sm='12'>
    <h2>{title}</h2>
    <p>
      {truncateString(body)} <br />
      {tags.map(tag => <Tag key={tag.id} name={tag.name} />)}
    </p>
    <p>
      <Link className='btn btn-secondary' to={`/blogs/${id}`} role='button'>
        View details »
      </Link>
    </p>
  </Col>
);

export default BlogTile;
