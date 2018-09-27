import React from 'react';
import { Switch, Route } from 'react-router-dom';

import BlogList from './list';
import CreateBlog from './create';
import Blog from './detail';

const Blogs = ({ match: { path } }) => (
  <Switch>
    <Route exact path={path} component={BlogList} />
    <Route path={`${path}/create`} component={CreateBlog} />
    <Route path={`${path}/:id`} component={Blog} />
  </Switch>
);

export default Blogs;
