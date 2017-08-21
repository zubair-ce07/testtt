import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import { BrowserRouter, Route, Switch } from 'react-router-dom'
import promise from 'redux-promise';
import reducers from './reducers';

import Login from './containers/login';
import Signup from './containers/signup';
import NewsDetail from './containers/news_detail';
import NewsHome from './containers/news_home';
import NewsSearchList from './containers/news_search';
import CategoryNewsList from './containers/category_news_list'
import Profile from './containers/profile';
import Test from './components/test'
import NavigationBar from './containers/nav_bar';

const createStoreWithMiddleware = applyMiddleware(promise)(createStore);

ReactDOM.render(
  <Provider store={createStoreWithMiddleware(reducers)}>
    <BrowserRouter>
      <div>
        <NavigationBar />
        <Switch>
          <Route path="/test" component={ Test } />
          <Route path="/profile" component={ Profile } />
          <Route path="/login" component={ Login } />
          <Route path="/signup" component={ Signup } />      
          <Route path="/news/categories/:name" component={ CategoryNewsList } />
          <Route path="/news/search/:query" component={ NewsSearchList } />
          <Route path="/news/:id" component={ NewsDetail } />
          <Route path="/news" component={ NewsHome }>
          </Route>
        </Switch>
      </div>
    </BrowserRouter>
  </Provider>
  , document.querySelector('.container'));
