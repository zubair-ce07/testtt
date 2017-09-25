import React from 'react';
import ReactDOM from 'react-dom';
import promise from 'redux-promise';
import thunk from 'redux-thunk';
import {Provider} from 'react-redux';
import {applyMiddleware, createStore, compose} from 'redux';
import {BrowserRouter, Route, Switch} from 'react-router-dom';

import reducers from './reducers';
import App from './components/app';
import HomePage from './components/home_page';
import SearchPage from './components/search_page';
import LoginPage from './components/login/login_page';
import SignupPage from './components/signup/signup_page';
import ProfilePage from './components/profile_page';
import MovieDetail from './components/movie_detail';
import WatchListPage from './components/watchlist_page';
import NetworkPage from './components/network_page';
import CalendarPage from './components/calendar_page';
import GenresPage from './components/genre_page';
import setAuthorizationToken from './utils/setAuthorizationToken';
import {setCurrentUser} from './actions/auth_actions'


const store = createStore(
    reducers,
    compose(applyMiddleware(promise, thunk), window.devToolsExtension ? window.devToolsExtension() : f => f)
);

if (localStorage.user) {
    setAuthorizationToken(JSON.parse(localStorage.user).token);
    store.dispatch(setCurrentUser(JSON.parse(localStorage.user)));
}

ReactDOM.render(
    <Provider store={store}>
        <BrowserRouter>
            <App>
                <Switch>
                    <Route path="/network/:type" component={NetworkPage}/>
                    <Route path="/movies/:movie_id" component={MovieDetail}/>
                    <Route path="/users/:user_id" component={ProfilePage}/>
                    <Route path="/watchlist/:status" component={WatchListPage}/>
                    <Route path="/genres/:genre_id" component={GenresPage}/>
                    <Route path="/calendar/" component={CalendarPage}/>
                    <Route path="/search/" component={SearchPage}/>
                    <Route path="/login/" component={LoginPage}/>
                    <Route path="/signup/" component={SignupPage}/>
                    <Route path="/" component={HomePage}/>
                </Switch>
            </App>
        </BrowserRouter>
    </Provider>,
    document.querySelector('#app')
);
