import React, { Component, Fragment } from 'react';
import { Link } from 'react-router-dom';

import { Button } from 'reactstrap';

import Comments from '../comments';
import Tag from '../tags/tag';

class BlogDetail extends Component {
  constructor(props) {
    super(props);

    this.id = +props.match.params.id;
  }

  componentDidMount() {
    if (!this.id) {
      this.props.history.push('/404');
      return;
    }

    this.props.loadBlogDetail(this.id);
  }

  render() {
    const {
      blog: { id, title, body, tags, writer },
      signedInUserId
    } = this.props;
    return (
      <Fragment>
        {signedInUserId === writer &&
          <Button
            tag={Link}
            to={`/blogs/edit/${id}`}
            color='primary'
            className='edit-button'
          >
            Edit
          </Button>
        }
        <h2>{title}</h2>
        <pre style={{ whiteSpace: 'pre-wrap' }}>
          {body} <br />
          {tags.map(tag => <Tag key={tag.id} name={tag.name} />)}
        </pre>
        <Comments blogId={this.id} />
      </Fragment>
    );
  }
}

export default BlogDetail;
