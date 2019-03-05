import React, { Component } from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import { Container } from 'reactstrap';
import { NotificationContainer } from 'react-notifications';

import NavBar from './nav-bar';
import Users from './users';
import Blogs from './blogs';
import NotFound from './not-found';

// import sampleContainer from '../redux/containers/simple.container';

import 'bootstrap/dist/css/bootstrap.css';
import 'react-notifications/lib/notifications.css';
import './app.css';

class App extends Component {
  render() {
    return (
      <div>
        <NavBar />
        <main>
          <Container>
            <Switch>
              <Redirect exact from='/' to='/blogs' />
              <Route path='/blogs' component={Blogs} />
              <Route path='/users' component={Users} />
              <Route path='/404' component={NotFound} />
              <Redirect to='/404' />
            </Switch>
          </Container>
        </main>
        <NotificationContainer />
      </div>
    );
  }
}

export default App;
