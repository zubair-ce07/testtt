import React from 'react';

import { Link } from 'react-router';
import { connect } from 'react-redux';
import { LogoutUser } from "../actions/LogoutUser";

class Navbar extends React.Component{
    render()
    {
        return(
            <nav className="navbar navbar-inverse">
                <div className="navbar-header">
                    <a className="navbar-brand" href="#">MyFacebook</a>
                </div>
                <div className="collapse navbar-collapse">
                    <ul className="nav navbar-nav">
                        <li><Link to={'/news'}>News</Link></li>
                    </ul>
                    <ul className="nav navbar-nav navbar-right">
                        <li>
                            <button className="navbar-btn btn btn-link" onClick={() => {
                                this.props.LogoutUser()}}>
                                <span className="glyphicon glyphicon-log-out">Logout</span>
                            </button>
                      </li>
                    </ul>
                </div>
            </nav>
        );
    }
}
export default connect(null, {LogoutUser})(Navbar)