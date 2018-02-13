import { Link, withRouter } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import React from 'react';

import PropTypes from 'prop-types'

import * as Actions from '../action.jsx'

class Menu extends React.Component {
    static propTypes = {
        username: PropTypes.string,
    };
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
                        <b>Freelancer:</b> {this.props.username} <b className="caret"></b>
                        </a>
                         <ul className="dropdown-menu">
                            <li><a><i className="fa fa-user"></i> Profile</a></li>
                            <li><i className="fa fa-sign-out"></i><Link to="/logout">Logout</Link></li>
                        </ul>
                    </li>
                </ul>
            </div>
        );
    }
}

function mapStateToProps(state) {
  return {
    username: state.nav_reducer.user,
    // token: state.login_reducer.token
  };
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(Actions, dispatch)
  };
}
export default withRouter(connect(
  mapStateToProps,
  mapDispatchToProps
)(Menu));

