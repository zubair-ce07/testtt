import React from 'react';
import { connect } from 'react-redux';
import { Link } from 'react-router';

import { logoutUser } from '../actions/logout_user';
import SearchBar from './searchbar';


class NavBar extends React.Component
{
    render()
    {
        return (
            <nav className="navbar navbar-inverse">
                <div className="container-fluid">
                    <div className="navbar-header">
                        <button type="button" className="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                            <span className="icon-bar"/>
                            <span className="icon-bar"/>
                            <span className="icon-bar"/>
                        </button>
                        <a className="navbar-brand" href="#">WebSiteName</a>
                    </div>
                    <div className="collapse navbar-collapse" id="myNavbar">
                        <ul className="nav navbar-nav">
                            <li><Link to="/profile">Profile</Link></li>
                        </ul>
                        <ul className="nav navbar-nav navbar-right">
                            <li>
                                <button className="navbar-btn btn btn-link" onClick={() => {
                                    this.props.logoutUser()
                                    }}>
                                    <span className="glyphicon glyphicon-log-out"/>{' '}Logout
                                </button>
                            </li>
                        </ul>
                        <SearchBar/>
                    </div>
                </div>
            </nav>
        );
    }
}

export default connect(null, { logoutUser })(NavBar);