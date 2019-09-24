import React from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { routeConstants } from './constants/routeConstants';

import Signup from './components/Signup';
import Login from './components/Login';
import Navbar from './components/Navbar';

const App = () => {
    return (
        <BrowserRouter >
            <div className="App">
                <Switch>
                    <Route exact path={routeConstants.LOGIN_ROUTE} component={Login} />
                    <Route exact path={routeConstants.SIGNUP_ROUTE} component={Signup} />
                    <Route path={routeConstants.NAV_BAR_ROUTE_ROUTE} component={Navbar} />
                </Switch>
            </div>
        </BrowserRouter>
    );
};
export default App;
