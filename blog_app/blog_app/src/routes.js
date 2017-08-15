import React from 'react';
import { Route, IndexRoute } from 'react-router';

import App from './components/app';
import BlogsIndex from './components/blogs';
import NewBlogPost from './components/new_blog_post';
import BlogDetails from './components/show_blog_post';

export default (
    <Route path="/" component={App}>
        <IndexRoute component={BlogsIndex}/>
        <Route path="/post/new" components={NewBlogPost} />
        <Route path="/post/:id" components={BlogDetails} />
    </Route>
);