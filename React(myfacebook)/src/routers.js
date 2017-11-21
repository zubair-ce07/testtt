import React from 'react';
import { Route } from 'react-router';

import NewsList from './components/NewsList';
import NewsDetail from './components/NewsDetail';

export default (
    <Route>
        <div>
            <Route exact path={"/"} component={ NewsList } />
            <Route path={"/news"} component={ NewsList } />
            <Route path={"/news/:id"} component={ NewsDetail } />
        </div>
    </Route>
);