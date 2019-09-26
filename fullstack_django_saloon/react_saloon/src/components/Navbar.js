import React from 'react';
import { Route, Switch, Link } from 'react-router-dom';
import { connect } from 'react-redux';
import ls from 'local-storage';
import PropTypes from 'prop-types';

import ListSaloon from './ListSaloon';
import Profile from './Profile';
import MySaloon from './MySaloon';
import SlotList from './SlotList';
import MyReservations from './MyReservations';

import { logout } from '../actions/userActions';
import { reactAppConstants } from '../constants/constants';
import { routeConstants } from '../constants/routeConstants';

import { AppBar, Toolbar, Typography,Button } from '@material-ui/core';

class Navbar extends React.Component {
    navBarStyle = {
        width: '100%'
    }

    logout = () => {
        this.props.logout(this.props.history);
    }

    userType = ls.get(reactAppConstants.USER_TYPE)
    token = ls.get(reactAppConstants.TOKEN)

    nav_bar_elements = this.token ? (
        <React.Fragment>
            <Typography variant="h6" color="inherit" style={{float: 'right'},{marginRight:'5px'}}>
                <Link style={{ textDecoration: 'none',color:'white' }} to={routeConstants.MY_RESERVATIONS_ROUTE}> My Reservations</Link>
            </Typography>
            {this.userType === reactAppConstants.SALOON && <Typography variant="h6" color="inherit" style={{float: 'right'},{marginRight:'5px'}}>
                <Link to={routeConstants.MY_SALOON_ROUTE} style={{ textDecoration: 'none',color:'white' }}> My Saloon</Link>
            </Typography>}
            <Typography variant="h6" color="inherit" style={{float: 'right'},{marginRight:'5px'}}>
                <Link to={routeConstants.PORFILE_ROUTE} style={{ textDecoration: 'none',color:'white' }}>Profile</Link>
            </Typography>
            <Button variant="contained" color="secondary" onClick={this.logout}>
                Logout
            </Button>
        </React.Fragment>
    ) : (<React.Fragment>
        <Typography variant="h6" color="inherit" style={{float: 'right'},{marginRight:'5px'}}>
            <Link to={routeConstants.LOGIN_ROUTE} style={{ textDecoration: 'none',color:'white' }}> Login</Link>
        </Typography>
        <Typography variant="h6" color="inherit" style={{float: 'right'},{marginRight:'5px'}}>
            <Link to={routeConstants.SIGNUP_ROUTE} style={{ textDecoration: 'none',color:'white' }}> Register</Link>
        </Typography>
    </React.Fragment>)

    render() {
        return (
            <React.Fragment>
                <AppBar position="static">
                    <Toolbar>
                        <Typography variant="h6" color="inherit" style={{flex: 1}}>
                            <Link to={routeConstants.LIST_SALOONS_ROUTE} style={{ textDecoration: 'none',color:'white' }}>Saloons</Link>
                        </Typography>
                        {this.nav_bar_elements}
                    </Toolbar>
                </AppBar>
                <Switch>
                    <Route exact path={routeConstants.LIST_SALOONS_ROUTE} component={ListSaloon} />
                    <Route exact path={routeConstants.PORFILE_ROUTE} component={Profile} />
                    <Route exact path={routeConstants.MY_SALOON_ROUTE} component={MySaloon} />
                    <Route exact path={routeConstants.MY_RESERVATIONS_ROUTE} component={MyReservations} />
                    <Route path={routeConstants.SLOT_LIST_ROUTE} component={SlotList} />
                </Switch>
            </React.Fragment >

        );
    }


}

Navbar.propTypes = {
    logout: PropTypes.func.isRequired,
    match: PropTypes.object.isRequired,
    history : PropTypes.object.isRequired
};

const mapDispatchToProps = dispatch =>
    (
        {
            logout: (history) => dispatch(logout(history))
        }
    );

export default connect(null, mapDispatchToProps)(Navbar);