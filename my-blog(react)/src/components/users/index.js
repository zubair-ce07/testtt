import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';


import SignUp from './sign-up';
import SignIn from './sign-in';

const Users = ({ match: { path } }) => (
  <Switch>
    <Route path={`${path}/signup`} component={SignUp} />
    <Route path={`${path}/profile`} component={SignUp} />
    <Route path={`${path}/signin`} component={SignIn} />
    <Redirect to='/404' />
  </Switch>
);

export default Users;
