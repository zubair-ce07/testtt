import React from 'react';
import { Switch, Route } from 'react-router-dom';


import SignUp from './sign-up';
import SignIn from './sign-in';
import Profile from './profile';

const Users = ({ match: { path } }) => (
  <Switch>
    <Route path={`${path}/signup`} component={SignUp} />
    <Route path={`${path}/signin`} component={SignIn} />
    <Route path={`${path}/profile`} component={Profile} />
  </Switch>
);

export default Users;
