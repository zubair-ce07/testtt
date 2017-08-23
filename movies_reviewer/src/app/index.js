import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import promise from 'redux-promise';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import reducers from './reducers';
import App from './components/app';
import MoviesIndex from './components/movies_index'
import MovieDetail from './components/movie_detail'

const createStoreWithMiddleware = applyMiddleware(
  promise
)(createStore);

ReactDOM.render(
    <Provider store={createStoreWithMiddleware(reducers)}>
        <BrowserRouter>
            <App>
                <Switch>
                    <Route exact path="/" component={MoviesIndex}/>
                    <Route path="/movies/:id" component={MovieDetail}/>
                </Switch>
            </App>
        </BrowserRouter>
    </Provider>,
    document.querySelector('#app')
);
