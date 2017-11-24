import React from 'react';
import { Route, IndexRoute } from 'react-router';

import Login from './components/Login'
import NewsList from './components/NewsList';
import NewsDetail from './components/NewsDetail';

export default (
    <Route path={'/'} >
        <IndexRoute component={ Login }/>
        <Route path={"/news"} component={ NewsList } />
        <Route path={"/news/:id"} component={ NewsDetail } />
    </Route>
);
