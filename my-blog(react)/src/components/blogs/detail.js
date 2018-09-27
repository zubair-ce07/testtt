import React, { Fragment } from 'react';
import { Link } from 'react-router-dom';

import { Badge } from 'reactstrap';

const Blog = () => (
  <Fragment>
    <h2>Heading</h2>
    <p>Donec id elit non mi porta gravida at eget metus. Fusce dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus. Etiam porta sem malesuada magna mollis euismod. Donec sed odio dui. <br /><Badge color="primary">Tag 1</Badge> <Badge color="primary">Tag 2</Badge></p>
    <p><Link className='btn btn-secondary' to='#' role='button'>View details »</Link></p>
  </Fragment>
);

export default Blog;
