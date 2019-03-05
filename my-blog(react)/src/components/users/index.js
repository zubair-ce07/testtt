import React from 'react';
import { Switch, Route, Redirect } from 'react-router-dom';

import SignIn from './sign-in';
import CreateUser from './create';

const Users = ({ match: { path } }) => (
  <Switch>
    <Route path={`${path}/signup`} component={CreateUser} />
    <Route path={`${path}/profile`} component={CreateUser} />
    <Route path={`${path}/signin`} component={SignIn} />
    <Redirect to='/404' />
  </Switch>
);

export default Users;
