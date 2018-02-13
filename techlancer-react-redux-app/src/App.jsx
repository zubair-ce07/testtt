import './App.css';

import { BrowserRouter } from 'react-router-dom';
import { Route, Switch } from 'react-router';
import React, { Component } from 'react';
import jQuery from 'jquery'

import Home from './home/home';
import Listing from './freelancer/listing/listing';
import LoginPage from './login/login-page';
import Logout from './login/logout';
import Nav from './nav/Nav';

global.jQuery = jQuery
global.jquery = jQuery
global.$ = jQuery

class App extends Component {
  render() {
    return(
      <BrowserRouter>
        <div>
          <Nav/>
          <Switch>
            <Route path="/freelancers" component={Listing}/> 
            <Route path="/login" component={LoginPage} />
            <Route path="/logout" component={Logout}/>
            <Route path="/" component={Home}/> 
          </Switch>
        </div>
      </BrowserRouter>
      );
  }
}

export default App;
