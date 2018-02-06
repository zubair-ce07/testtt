import React from 'react';
import User from '../../models/User.jsx';
import Auth from '../../services/auth.jsx';
import PropTypes from 'prop-types'
import {
  Link,
} from 'react-router-dom'

export default class Menu extends React.Component {
    static propTypes = {
        name: PropTypes.string,
    };
    constructor(props){
        super(props);
        let user = new User();
        this.state = {
            username:""
        };
        user.get().then((response) => {
            this.setState({
                username:response.username
            }) 
        });
    }
    logout(){
        let auth = new Auth();
        auth.reset();
    }
    render() {
        return (
            <div className="navbar-collapse collapse" id="bs-example-navbar-collapse-1" style={{height: 1 +'px'}}>
                <ul className="nav navbar-nav">
                    <li className="dropdown">
                        <a><i className="fa fa-tasks"></i> Jobs</a>
                    </li>
                    <li><Link to="/freelancers">Freelancers</Link></li>
                    <li>
                        <a className="dropdown-toggle" data-toggle="dropdown">
                        <i className="fa fa-user-circle"></i> 
                        <b>Freelancer:</b> {this.state.username} <b className="caret"></b>
                        </a>
                         <ul className="dropdown-menu">
                            <li><a><i className="fa fa-user"></i> Profile</a></li>
                            <li><i className="fa fa-sign-out" onClick={this.logout}></i><Link to="/" onClick={this.logout}>Logout</Link></li>
                        </ul>
                    </li>
                </ul>
            </div>
        );
    }
}

