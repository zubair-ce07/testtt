import React, { Component } from 'react';

import { Row } from 'reactstrap';

import BlogsService from './blogs.service';
import BlogTile from './blog-tile';


class BlogList extends Component {
  constructor(props) {
    super(props);

    this.state = {
      blogs: [],
    };

    this.service = new BlogsService();
  }

  async componentDidMount() {
    const response = await this.service.get();

    if (response.success) {
      this.setState({ blogs: response.data });
    }
  }

  render() {
    return (
      <Row>
        {
          this.state.blogs.map(blog => <BlogTile key={blog.id} blog={blog} />)
        }
      </Row>
    );
  }
}

export default BlogList;
