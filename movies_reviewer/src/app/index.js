import React from 'react';
import ReactDOM from 'react-dom';
import promise from 'redux-promise';
import {Provider} from 'react-redux';
import {applyMiddleware, createStore} from 'redux';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import reducers from './reducers';
import App from './components/app';
import NewReview from './components/add_review';
import MoviesIndex from './components/movies_index';
import MovieDetail from './components/movie_detail';
import ActorDetail from './components/actor_detail';

const createStoreWithMiddleware = applyMiddleware(
    promise
)(createStore);

ReactDOM.render(
    <Provider store={createStoreWithMiddleware(reducers)}>
        <BrowserRouter>
            <App>
                <Switch>
                    <Route exact path="/" component={MoviesIndex}/>
                    <Route exact path="/movies/:movie_id/reviews" component={NewReview}/>
                    <Route path="/movies/:id" component={MovieDetail}/>
                    <Route path="/actors/:id" component={ActorDetail}/>
                </Switch>
            </App>
        </BrowserRouter>
    </Provider>,
    document.querySelector('#app')
);
