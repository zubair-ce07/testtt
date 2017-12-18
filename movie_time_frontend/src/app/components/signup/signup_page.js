import React, {Component} from 'react';
import {connect} from "react-redux";

import SignupFrom from './signup_form';


class SignupPage extends Component{
    componentWillMount() {
        if (this.props.isAuthenticated) this.props.history.push('/');
    }

    render(){
        return (
            <div>
                <SignupFrom history={this.props.history}/>
            </div>
        );
    }
}

function mapStateToProps({auth_user}) {
    return {isAuthenticated: auth_user.isAuthenticated};
}

export default connect(mapStateToProps)(SignupPage);
