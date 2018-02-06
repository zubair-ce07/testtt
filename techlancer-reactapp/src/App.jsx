import 'bootstrap/dist/css/bootstrap.min.css';

import './index.css';

import {
  Redirect,
  Route,
  BrowserRouter as Router,
  Switch,
} from 'react-router-dom';
import React, { Component } from 'react';
import jQuery from 'jquery'

import Auth from './services/auth';
import Home from './home/home.jsx';
import Listing from './freelancer/listing/listing';
import LoginPage from './login/login-page.jsx'
import Nav from './nav/Nav';
import Profile from './freelancer/profile/Profile.jsx';
import Signup from './signup/signup';

global.jQuery = jQuery
global.jquery = jQuery // jquery lowercase  was the solution
global.$ = jQuery


export default class App extends Component {

  constructor(props) {
    super(props);
    let auth = new Auth();
    // set the initial component state
    this.state = {
      loggedIn : auth.isAuthenticated()
    };  

    this.login = this.login.bind(this);
  }

  login(isAuthenticated) {
    this.setState(
      {loggedIn : isAuthenticated}
    )
  }


  render() {
    return (
        <Router>
          <div>
            <Nav/>
            <Switch>
              <Route exact path='/' component={Home}/>
              <Route exact path="/login" render={() => (
                this.state.loggedIn ? (
                  <Redirect to="/"/>
                ) : (
                  <LoginPage onLogin={this.login} />
                )
              )}/>
              <Route exact path='/register' component={Signup} />
              <Route exact path='/register' component={Signup} />
              <Route exact path='/profile' component={Profile} />
              <Route exact path='/freelancers' component={Listing} />
            </Switch>
          </div>
         </Router>
    );
  }
}
