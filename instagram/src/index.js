import React from 'react';
import ReactDOM from 'react-dom';
import {Route, Router} from 'react-router';
import createBrowserHistory from 'history/createBrowserHistory';

import Signup from './insta/components/signup'

const history = createBrowserHistory();

class Routes extends React.Component{
    render() {
        return(
            <Router history={history}>
                <Route exact path="/" component={Signup}/>
            </Router>
        )
    }
}

ReactDOM.render(
    <Routes/>,
    document.getElementById('root')
);