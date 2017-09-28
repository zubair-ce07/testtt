import React, { Component } from 'react';
import { connect } from 'react-redux';
import LoginHandler from '../Auth/Login';
import Secured from './Secured';
import NotFound from '../NotFound'
import UserProfile from '../Users/UserProfile'
import MainNav from './MainNav'

import createHistory from 'history/createBrowserHistory'
import { Route, Redirect, Router, Switch } from 'react-router'

const history = createHistory()
 
class SocialNetwork extends Component {
    render() {
        if (this.props.isLoggedIn) {
            return (
                    <Router history={history}>
                        <div>
                            <MainNav />
                            <Switch>
                                <Route path="/" exact component={Secured} />
                                <Route path="/profile/:id" exact component={UserProfile}/>
                                <Redirect from="/login" to="/" />
                                <Route path="*" component={NotFound} />
                            </Switch>
                        </div>
                    </Router>
                );
        } 
        else{
            return (
                    <Router history={history}>
                            <div>
                                <Redirect to="/login" />
                                <Route path="/login" component={LoginHandler} />
                            </div>
                    </Router>
                );
        }
    }
}
 
const mapStateToProps = (state, ownProps) => {
    return {
        isLoggedIn: state.authReducer.isLoggedIn,
        username: state.authReducer.username,
        id: state.authReducer.id
    };
}

export default connect(mapStateToProps)(SocialNetwork);