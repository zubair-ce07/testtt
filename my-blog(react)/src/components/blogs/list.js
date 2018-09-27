import React from 'react';

import { Row } from 'reactstrap';

import BlogTile from './blog-tile';

const BlogList = () =>
  <Row>
    <BlogTile />
    <BlogTile />
    <BlogTile />
    <BlogTile />
  </Row>;

export default BlogList;
