import React, { Component } from 'react';

import { Row, Col } from 'reactstrap';

import BlogTile from './blog-tile';


class BlogList extends Component {
  componentDidMount() {
    this.props.loadBlogs();
  }

  render() {
    const { loaded, blogs } = this.props;
    return (
      <Row>
        {
          blogs.map(blog => <BlogTile key={blog.id} blog={blog} />)
        }
        {
          loaded && !blogs.length &&
          <Col><h3>No Blog added yet!</h3></Col>
        }
      </Row>
    );
  }
}

export default BlogList;
