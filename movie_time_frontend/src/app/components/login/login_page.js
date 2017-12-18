import React, {Component} from 'react';
import {connect} from "react-redux";

import LoginFrom from './login_form';


class LoginPage extends Component{
    componentWillMount() {
        if (this.props.isAuthenticated) this.props.history.push('/');
    }

    render(){
        return (
            <div>
                <LoginFrom history={this.props.history}/>
            </div>
        );
    }
}

function mapStateToProps({auth_user}) {
    return {isAuthenticated: auth_user.isAuthenticated};
}

export default connect(mapStateToProps)(LoginPage);
